# Research: measuring note quality

Issue #26, researched 2026-10-30. The benchmark measures only capture coverage. This note asks what
could measure note quality. Lines marked **Inference** are mine; the rest is sourced. It picks no
measure.

## Summary and note evaluation

- **Question-based, from source to output.** These generate questions from the source and check
  that the output answers them. QuestEval's average Pearson correlation with human ratings was
  0.335 with no reference, against 0.118 for ROUGE-1 with one reference
  ([Scialom 2021](https://arxiv.org/abs/2103.12693)). Those ratings are expert opinions on short
  news summaries, not learning. Component choice matters: tuning gave QAFactEval a 14% average gain
  over earlier QA metrics ([Fabbri 2022](https://arxiv.org/abs/2112.08542)). Both date from 2021–22.
- **Claim-based, from output to source.** FActScore splits text into atomic facts and reports the
  share a knowledge source supports. Human checking cost about $4 per generation
  ([Min 2023](https://arxiv.org/abs/2305.14251)). It measures precision, so it can't see omissions.
- **Human decomposition.** QAPyramid reached Krippendorff's alpha 0.74 but needs a reference
  summary and took about 380 annotator hours to judge 50 examples across 10 systems
  ([Zhang 2024](https://arxiv.org/abs/2412.07096)).

### Do automated scores track learning?

Only weakly, and the evidence is thin.

- The closest study had 150 crowdworkers read plain-language medical summaries at $1 per pair.
  LLM and human summaries looked alike in ratings, yet human ones gave better multiple-choice
  accuracy. Of 10 metrics, only QA-based QAEval predicted comprehension (β 0.039, p 0.035, N 459);
  ROUGE did not (β −0.001). Human ratings did predict it, at similar size
  ([Guo 2025](https://arxiv.org/abs/2505.10409)). Each summary had three questions, answered in
  the same task.
- An older task study of ten people found positive ROUGE correlations with a relevance-judging
  task, none significant at p < 0.05 ([Dorr 2005](https://aclanthology.org/W05-0901/)).
- I found no study linking automated scores to learning from long notes or video, or to delayed
  retention.

## LLM judges

They agree with people more on facts than on preference, and they lean generous.

- **Agreement is overstated.** Strong judges matched human agreement at over 80% in 2023
  ([Zheng](https://arxiv.org/abs/2306.05685)). Across 21 judges, exact match overstated
  chance-corrected agreement by 38.6 points on average on a preference benchmark; Claude Opus 4.6
  went from 84.8% to κ 0.489. High test-retest scores can coexist with severe position bias
  ([Norman 2026](https://arxiv.org/abs/2606.19544)).
- **Leniency moves with design.** On binary answer grading, judges averaged 96.5% accuracy, but
  detailed prompts shifted leniency by 28.9 points and switching models by up to 56.1
  ([Vaugrante 2026](https://arxiv.org/abs/2610.05094)).
- **No reference, more credit.** Without a reference, judges can over-credit wrong answers: clearest
  in Telugu, while English and Arabic looked reasonably calibrated. Adding one flipped 9–85% of
  verdicts ([Kranti 2026](https://arxiv.org/abs/2607.12885)).
- **Style.** Identical content in markdown beat plain prose: judges preferred it 73–97% of the time
  (four of five), humans 57% on a 30-pair sample. Position bias was at most 0.04 there
  ([Soumik 2026](https://arxiv.org/abs/2604.23178)). Verbosity findings conflict: model-specific
  there, almost none in Norman.
- **Familiar text.** GPT-4 favours its own output, apparently because it is familiar
  ([Wataoka 2024](https://arxiv.org/abs/2410.21819)). Small-to-mid judges rarely chose the human
  summary over an LLM one ([Fang 2026](https://arxiv.org/abs/2602.07673)).
- **Long text.** Verdicts vary more as the text grows, so Anthropic advises keeping `llm` graders
  to short outputs ([Claude Code docs](https://code.claude.com/docs/en/plugin-evals)).

**What reduces this:** code checks first; concrete PASS/FAIL rubrics; a reference; an "Unknown"
option and one judge per dimension; calibrating against human grades
([Anthropic, Jan 2026](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents));
reporting κ with both presentation orders (Norman). Chain-of-thought plus order swapping gained up
to 11.5 points, though swapping alone hurt on adversarial cases (Soumik). Expect criteria drift:
grading changes your criteria ([Shankar 2024](https://arxiv.org/abs/2404.12272)).

**An LLM is a poor stand-in for a learner.** Persona-prompted models scored 0.96–0.99 on reading
tests where primary-school students averaged 0.69
([Balog 2026](https://arxiv.org/abs/2608.30033)). On linguistics puzzles, told to
abstain when information was missing, three frontier models rarely did, and often stayed correct
([Majmudar 2026](https://arxiv.org/abs/2608.27756)).

**Inference:** a model reading the notes can fill gaps from what it already knows, which is the main
threat to checks 1 and 6 in step 7. No source validated an LLM judge against learning outcomes.

## How agent skills are evaluated

- **Agent Skills.** The [spec](https://agentskills.io/specification) covers format only;
  `skills-ref` validates frontmatter. A separate
  [guide](https://agentskills.io/skill-creation/evaluating-skills) sets the method: start with 2–3
  cases, run each with and without the skill, require evidence for each PASS, drop assertions that
  pass in both arms, and leave qualities like style to human review.
- **Anthropic.** [Best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
  asks for three evaluations against a baseline and says no built-in runner exists. That note looks
  stale: [skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator)
  ([March 2026](https://claude.com/blog/improving-skill-creator-test-measure-and-refine-agent-skills))
  runs paired evals, benchmarks and blind comparison, and `claude plugin eval` reports WITH, W/OUT
  and Δ, at about cases × runs × 2 agent runs (3 runs by default).
- **OpenAI.** 10–20 prompts, scripted checks on the trace, a schema-bound model rubric for the rest
  ([undated post](https://developers.openai.com/blog/eval-skills)).
- **NVIDIA.** Paired live runs in [SkillEvaluator](https://docs.nvidia.com/skills/evaluating-agent-skills.md).
  Static scan scores had no correlation with live lift on 62 skills
  ([Kevin 2026](https://arxiv.org/abs/2608.20614)).
- **SkillsBench.** 87 tasks with deterministic verifiers, deliberately no LLM judge: pass rate rose
  from 33.9% to 50.5% with skills, while comprehensive documentation added 0.7 points
  ([Li 2026](https://arxiv.org/abs/2602.12670)).

**Inference:** the shared pattern is a paired baseline, code checks where possible, a small case set
and human review. None of it asks whether a person learned anything.

## Candidate methods

Everything in this table is **inference** about this skill. No method has been tried on it.

| Method | Needs | Would tell us | Wouldn't tell us |
| --- | --- | --- | --- |
| **Closed-book quiz**: step 7's quiz, answered with the notes and again without them | No labels or people; a few cheap calls per video on saved notes | Which transcript facts the notes add beyond what the model knows | On-screen-only content; human learning |
| **On-screen recall**: is each state in `bench/labels` present in the notes? | Existing labels (422 states, 7 videos; 3 videos' labels have no human check); notes for those videos; one call per state | Whether caught frames reach the notes; ties to capture coverage | Whether the state is explained well |
| **Hands-on replay**: a fresh agent follows the cheat sheet in a sandbox, a script checks the result | A hand-written verifier per tutorial; a sandbox; agent tokens | "Can do what it teaches", with no judge | Conceptual videos; gaps the agent fills itself |
| **Claim check**: FActScore-style, against transcript and fetched sources | Tokens per claim; your grades on a sample | Invented or mis-tagged content | Omissions; visuals |
| **Human comprehension test**: fresh readers take a quiz written from the video | A few readers per video, none of whom has seen it | Real learning, and whether the proxies track it | Much, statistically, at small n; long-term retention |
| **Owner review**: `feedback.json` per case | Your time | Problems nobody thought to test | Anything reproducible; drifts |
| **Blind version comparison** | Tokens only | Which version a judge prefers | Learning; exposed to style and familiarity bias, since the page is designed |
| **Paired no-skill run** | Full runs × 2; cost unmeasured | Regressions and skill lift | Note quality on its own: a no-skill agent may mostly fail on tooling |
| **Off-the-shelf metrics** (QuestEval, QAFactEval) | Setup | Little: built on short news | Learning, on any evidence I found |
| **QAPyramid** | Hundreds of annotator hours; a reference summary, which notes lack | Content selection | Out of budget |

## What this means for the decision

**Inference throughout.**

- Step 7 already holds two of these unpaired: the cold-reader test and the optional quiz. Without a baseline,
  the quiz's 95% bar can't separate notes that teach from a model that already knew. Nothing in
  these sources supports that bar.
- Transcript coverage is necessary but not sufficient: a mapped chunk may still not be taught.
- Keep judge inputs short and factual: one question or claim at a time, with the source as
  reference, on extracted text rather than the designed page.
- Grade saved notes separately from generating them, so re-grading stays cheap.

Ranked shortlist for one person with a small budget:

1. **Closed-book quiz**, with roughly 30–50 answers graded by hand to report κ. Cheapest; reuses an
   existing check.
2. **Hands-on replay** on one or two tutorials. Closest to "do what it teaches", with no judge.
3. **On-screen recall.** Reuses existing labels and covers the gap in 1.
4. **Claim check**, calibrated on a sample. Covers wrong content, which 1–3 miss.
5. **Human comprehension test**, run once on a few videos, to see whether 1 tracks real readers.
   Costliest, and the only one that observes learning.

Owner review runs alongside these. A holistic judge score isn't shortlisted: every bias above
applies, and nothing links it to learning.

## What I couldn't verify

- A full skill run's token cost isn't known, so no method has a real budget figure.
- `claude plugin eval` and skill-creator weren't run; their fit for long video jobs is untested.
- Most 2026 papers here are arXiv preprints, Soumik (TMLR) aside, and judge results age quickly. None
  tests a judge on long study notes.
- Zheng, Wataoka and Shankar were read as abstracts only; QAEval's result comes from Guo 2025. The
  Anthropic engineering and skill-creator posts, the skill-creator file, and the OpenAI and NVIDIA
  pages went through a summarising fetch. Long papers were read in part, with figures checked against
  the paper text.
