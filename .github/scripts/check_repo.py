"""Repository checks run by CI (and locally: python3 .github/scripts/check_repo.py).

- SKILL.md frontmatter against the Agent Skills spec (https://agentskills.io/specification),
  and that every scripts/, references/ and assets/ path it mentions exists
- .claude-plugin/plugin.json and marketplace.json: required fields, names and paths agree
- versions agree: plugin.json, SKILL.md metadata, and a matching CHANGELOG heading
- every Python file compiles, with SyntaxWarnings treated as errors
- notebook code cells compile (IPython "!" lines skipped)
- no stray control characters in text files (an invisible backspace once broke a regex here)
- YAML under .github parses (when PyYAML is installed)
Exits 1 and lists every failure.
"""
import json
import re
import sys
import warnings
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / "skills" / "video-notes"
failures = []


def fail(msg):
    failures.append(msg)


def frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None, text
    raw, body = m.group(1), text[m.end():]
    try:
        import yaml
        return yaml.safe_load(raw), body
    except ImportError:
        pass
    data, key = {}, None
    for line in raw.splitlines():                      # minimal parser: top-level keys, one map
        if re.match(r"^[A-Za-z][\w-]*:", line):
            key, _, val = line.partition(":")
            val = val.strip()
            data[key] = val.strip('"') if val else {}
        elif key and line.startswith("  ") and isinstance(data.get(key), dict):
            k, _, v = line.strip().partition(":")
            data[key][k] = v.strip().strip('"')
    return data, body


# ---- SKILL.md ----
skill_md = (SKILL / "SKILL.md").read_text(encoding="utf-8")
fm, body = frontmatter(skill_md)
if fm is None:
    fail("SKILL.md: no YAML frontmatter")
    fm = {}
allowed = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
for k in set(fm) - allowed:
    fail(f"SKILL.md: frontmatter field '{k}' isn't in the Agent Skills spec")
name = str(fm.get("name", ""))
if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name) or len(name) > 64:
    fail(f"SKILL.md: name '{name}' must be 1-64 lowercase letters, digits and single hyphens")
if name != SKILL.name:
    fail(f"SKILL.md: name '{name}' must match its folder '{SKILL.name}'")
desc = str(fm.get("description", ""))
if not 1 <= len(desc) <= 1024:
    fail(f"SKILL.md: description must be 1-1024 characters (is {len(desc)})")
if "compatibility" in fm and not 1 <= len(str(fm["compatibility"])) <= 500:
    fail("SKILL.md: compatibility must be 1-500 characters")
meta = fm.get("metadata") or {}
if not isinstance(meta, dict) or not all(isinstance(v, str) for v in meta.values()):
    fail("SKILL.md: metadata must map strings to strings (quote numbers, e.g. version: \"1.2.0\")")
if skill_md.count("\n") >= 500:
    fail("SKILL.md: keep it under 500 lines (move detail to references/)")
for ref in sorted(set(re.findall(r"`(?:python3 )?((?:scripts|references|assets)/[\w./-]+)", body))):
    if not (SKILL / ref.rstrip("/")).exists():
        fail(f"SKILL.md mentions {ref}, which doesn't exist")

# ---- plugin manifests and versions ----
try:
    plugin = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
    market = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))
except (OSError, ValueError) as e:
    fail(f".claude-plugin: {e}")
    plugin, market = {}, {}
if plugin:
    if not plugin.get("name"):
        fail("plugin.json: 'name' is required")
    for k in ("name", "owner", "plugins"):
        if k not in market:
            fail(f"marketplace.json: '{k}' is required")
    entries = {p.get("name"): p for p in market.get("plugins", [])}
    if plugin.get("name") not in entries:
        fail("marketplace.json: no entry with plugin.json's name")
    for p in market.get("plugins", []):
        src = p.get("source")
        if isinstance(src, str) and (".." in src or not (ROOT / src).exists()):
            fail(f"marketplace.json: source '{src}' must be a path inside the repo")
    version = plugin.get("version", "")
    if meta.get("version") != version:
        fail(f"version mismatch: plugin.json {version!r}, SKILL.md metadata {meta.get('version')!r}")
    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    if f"## [{version}]" not in changelog:
        fail(f"CHANGELOG.md has no '## [{version}]' heading for the current version")
    if "## [Unreleased]" not in changelog:
        fail("CHANGELOG.md needs an '## [Unreleased]' section")

# ---- Python compiles, warnings as errors ----
py_files = [p for p in ROOT.rglob("*.py") if ".git" not in p.parts and "node_modules" not in p.parts]
for p in py_files:
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        try:
            compile(p.read_text(encoding="utf-8"), str(p), "exec")
        except (SyntaxError, SyntaxWarning, ValueError) as e:
            fail(f"{p.relative_to(ROOT)}: {e}")

# ---- notebooks ----
for nb_path in ROOT.rglob("*.ipynb"):
    if ".git" in nb_path.parts:
        continue
    try:
        nb = json.loads(nb_path.read_text(encoding="utf-8"))
    except ValueError as e:
        fail(f"{nb_path.relative_to(ROOT)}: invalid JSON: {e}")
        continue
    for i, cell in enumerate(nb.get("cells", [])):
        if cell.get("cell_type") != "code":
            continue
        src = "".join(cell.get("source", []))
        py = "\n".join(re.sub(r"^(\s*)!.*", r"\1pass", line) for line in src.splitlines())
        try:
            compile(py, f"{nb_path.name} cell {i}", "exec")
        except SyntaxError as e:
            fail(f"{nb_path.relative_to(ROOT)}: code cell {i}: {e}")

# ---- control characters ----
text_ext = {".py", ".md", ".json", ".ipynb", ".yml", ".yaml", ".txt", ".html", ".toml", ".cfg"}
for p in ROOT.rglob("*"):
    if ".git" in p.parts or not p.is_file() or (p.suffix not in text_ext and p.name not in (".gitignore", ".gitattributes")):
        continue
    for n, line in enumerate(p.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        bad = [c for c in line if ord(c) < 32 and c not in "\t\r"]
        if bad:
            fail(f"{p.relative_to(ROOT)}:{n}: control character {bad[0]!r}")

# ---- YAML under .github ----
try:
    import yaml
    for p in list((ROOT / ".github").rglob("*.yml")) + list((ROOT / ".github").rglob("*.yaml")):
        try:
            yaml.safe_load(p.read_text(encoding="utf-8"))
        except yaml.YAMLError as e:
            fail(f"{p.relative_to(ROOT)}: {e}")
except ImportError:
    print("note: PyYAML not installed, skipping YAML checks")

if failures:
    print(f"{len(failures)} problem(s):")
    for f in failures:
        print("  -", f)
    sys.exit(1)
print(f"all checks passed ({len(py_files)} Python files)")
