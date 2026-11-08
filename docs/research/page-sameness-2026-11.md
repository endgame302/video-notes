# Keeping the notes pages worth opening (issue #44, stage 1)

Date: 2026-11-08

Stage 1 was researched without reading the issue's comments or the owner's earlier ideas. Stage 2 should read them and check this file against them.

Methods:

- A deep-research pass with five strands: consistency versus variety, surface variety, reading fatigue, why people stop, active versus passive learning. Plus a product survey.
- A finding-prior-art deep sweep of open-source projects, run together with the sweep in `docs/agents/tool-scouting.md`.
- A primary-source check of the report that these produced. It is described in the "Fact check" section. Numbers in this file are the checked ones. Numbers that could not be checked are marked "unverified summary".

How to read the reading status. "Full text" means the paper or page was read. "Abstract" means only the abstract was read. "Summary only" means the claim reached us through a search summary or secondary source.

## Fact check

The report's main claims were checked against the papers, the product pages and the GitHub repositories. Outcomes:

| Item | Outcome |
|---|---|
| Rowland 2014 (testing vs restudy) | Verified in full text. All numbers in 2.5 match (g 0.50; 0.69 and 0.41 by delay; 0.73 and 0.39 by feedback; 0.03 for first attempts at 50% or less with no feedback). |
| Yang et al. 2021 (classroom testing) | Verified in full text. All numbers match, including p = .062 for the effect against other active strategies and p = .119 for continuing education. The continuing-education effects all came from one study. |
| Pan and Rickard 2018 (transfer) | Verified in full text. 192 effects, 122 experiments, 67 articles, N = 10,382, d = 0.40. Corrected only by adding the article count. |
| Cepeda et al. 2006 (spacing) | Verified in full text. **Corrected**: "spaced beat massed at every interval" was too strong. See 2.5. |
| Dunlosky et al. 2013 | Verified in full text. Practice testing and distributed practice rated high utility. Rereading, highlighting and summarising rated low. |
| Adesope et al. 2017 | Abstract only (paywalled). The abstract has no numbers. The only numbers we have (g 0.51 against restudy; feedback 0.63 against 0.60) come from Yang et al.'s description. Unverified summary. |
| Learn Your Way (arXiv 2509.18664) | Verified in full text, v2. **Corrected**: more formats did not significantly predict scores, but the direction was positive and n was 30. Google also took part in design, collection and analysis. No journal version found. |
| Schneider et al. 2018 (signalling) | **Corrected**: the report linked a different meta-analysis. Numbers were confirmed through a clearinghouse summary of the right paper, not its abstract. See 2.1. |
| Sundararajan and Adesope 2020 (seductive details) | Abstract and a university press release only. The count (58 studies, over 7,500 students) is confirmed by the press release. **g about -0.33 is an unverified summary.** |
| Brom et al. 2018 (emotional design) | Verified in full text (author manuscript). All numbers match. Added: the authors found no moderation by time on task, and only one study was longer than 40 minutes. |
| Delgado et al. 2018 and Clinton-Lisell 2019 (screen vs paper) | Delgado 2018 verified in full text. Clinton-Lisell 2019 verified in abstract. **Corrected**: the report read the meta-analysis through a later paper. See 2.3. |
| Bisra et al. 2018 (self-explanation) | Verified in abstract. 69 effects, 64 reports, g = 0.55. |
| Kornell and Bjork 2008 | Verified in full text. **Corrected**: the "over 80% / about 15%" figures were loose. See 2.5. |
| Kizilcec et al. 2013 (MOOC disengagement) | Verified in full text. Sampling 39% in one course and 80% in another. Disengaging learners usually left in the first third. |
| Lally et al. 2010 (habit) | Abstract only (paper blocked). **Corrected**: the 66-day figure is not in the abstract. See 2.4. |
| Roediger and Karpicke 2006 | Abstract verified. The report's percentages were never used and stay out. |
| Pan and Carpenter 2023 (prequestions) | Abstract verified. No pooled size, as the report said. |
| Brunmair and Richter 2019 (interleaving) | Verified in abstract of the author manuscript. g = 0.42, 59 studies. **Added caveat**: effects were not significant for expository texts, and blocking beat interleaving for words. |
| Duolingo streak test | Verified on the company page. **Corrected**: +3.3% is a relative change, from a test that split the daily goal from the streak, not a test of streaks against no streaks. |
| take-notes, ELI5, explain-this | Repositories exist, all MIT. **Corrected**: take-notes does video in and designed HTML out, so "no full fit" needed a qualifier. See 3.2. |
| FSRS repositories and benchmark | Exist and are MIT, except the benchmark repository, which has no licence. **Corrected**: the log-loss figure labelled FSRS-7 belongs to the "recency" variant. See 3.2. |
| Barbieri 2023, Xie 2018 and critique, Raviv 2022, Kalyuga 2007, Hunt 1995, Hidi and Renninger 2006, Kang 2009, banner blindness, MOOC dropout review, NotebookLM, Readwise, Recall, Matuschak, Ground News, WR Publishing | Not rechecked. They stay as the report had them, marked "summary only" or "abstract" in the sources table. |
| The 13 baseline pages (section 4) | Not rechecked. The measurements were made locally and the pages were not reopened for this check. |

Net effect on the answer: it does not change. Two statements were weakened (spacing at every interval; "no project does video in, designed page out"). No recommendation moved.

## 1. Answer in 2-3 sentences

Do not restyle the pages to fight sameness. The evidence says the thing that earns a return visit is that the reader has to retrieve something, ideally spaced over days, and the look of the page has no good evidence behind it. Keep the stable frame, make the content correct, complete and doable, and add a short "try before you look" step and a watch-moment log. Then test the change on a few real pages before committing to it.

## 2. Learning evidence

### 2.1 Consistency versus variety

No study found tests a fixed document template repeated over weeks against a varied one, with later use or learning as the outcome. This is the main gap in the literature I could reach.

What exists is indirect. Making structure explicit helps. Schneider et al. 2018 pooled 103 studies (12,201 participants). Signalling gave retention g = 0.53 (139 comparisons) and transfer g = 0.33 (70 comparisons). Most studies were short lab lessons. This was read through a clearinghouse summary of the paper, not its abstract. It supports keeping the structural cues that tell the reader where things are. It says nothing about repeating a visual look. A separate meta-analysis of signalling that links text and pictures (Richter et al. 2016: 27 studies, 45 comparisons, N = 2,464) found r = 0.17 for transfer and comprehension, larger for readers with low prior knowledge ([Richter et al. abstract](https://doi.org/10.1016/j.edurev.2015.12.003)). The report had linked this paper by mistake.

The "readers go blind to a familiar layout" worry rests on banner blindness. That is usability work on ads in fixed positions, not on study text the reader chose to open (summary only, not rechecked) ([jnd.org](https://jnd.org/banner-blindness-human-cognition-and-web-design/)). It is a weak analogy.

A better-grounded worry is expertise reversal. Guidance that helps novices can become redundant for people who know more, and the relative value of a format can reverse (reviews, summary only, not rechecked) ([Kalyuga 2007](https://www.uky.edu/~gmswan3/EDC608/Kalyuga2007_Article_ExpertiseReversalEffectAndItsI.pdf)). A fixed scaffold may help on page 1 and be dead weight on page 13. My inference, untested: if a reader skims, redundancy is a likelier cause than layout familiarity.

The isolation (von Restorff) effect points the other way for variety. An item is remembered because it differs from a constant surround. That was shown with word lists, and no meta-analysis was found (summary only, not rechecked) ([Hunt 1995](https://link.springer.com/content/pdf/10.3758/bf03197149.pdf)). My inference: a stable frame makes the one changing thing more visible.

### 2.2 Does surface variety help or hurt?

Decoration unrelated to the content hurts. A seductive-details meta-analysis covered 58 studies and over 7,500 students. Most sessions lasted 6 to 12 minutes. The harm was larger when the detail sat beside relevant diagrams, when it was static, and on paper. The count and moderators come from a university press release and the abstract. The size, g about -0.33, is an unverified summary ([Sundararajan and Adesope 2020](https://doi.org/10.1007/s10648-020-09522-4)).

Purposeful visual design shows small gains in short sessions. Adding faces or pleasant colour to instructional graphics gave retention d+ 0.387, comprehension 0.317, transfer 0.327 and intrinsic motivation 0.255, but liking only 0.109. This was 33 samples, N = 2,924, mostly college students on science content, self-paced sessions up to about 30 minutes, with one study over 40 minutes. The authors name a novelty effect that fades over longer study as a possible moderator. Their analysis found no moderation by time on task, but with one long study it could not have shown one (full text) ([Brom et al. 2018](https://artemis.ms.mff.cuni.cz/main/papers/emodesign_manuscript_1rev_180928_FINAL_norev.pdf)). So these gains cannot say anything about week-three behaviour.

Novelty effects on technology-based learning are mixed. A math-software meta-analysis found larger effects for 0-4 week uses (1.193) than for longer ones (0.535). Other reviews found no such drop. None tests document format (summary only, low confidence, not rechecked) ([review](https://link.springer.com/article/10.1186/s41239-021-00314-6)).

Fluency tricks do not help either. A meta-analysis of perceptual disfluency (25 studies, text recall and transfer) found near-null pooled effects. A 2020 critique found coding errors, so "null" is shaky for recall and sturdier for transfer (summary only, not rechecked) ([critique](https://link.springer.com/article/10.1007/s10648-020-09579-1)).

### 2.3 Reading fatigue

Screen reading carries a small comprehension cost. Delgado et al. 2018 pooled 54 comparisons (38 between-participant, 16 within-participant; 171,055 participants) and found Hedges' g = -0.21 favouring paper. For informational texts it was -0.27 and for mixed texts -0.30. For narrative-only texts it was +0.01. The paper advantage was g = -0.26 when reading time was limited and -0.09 (confidence interval -0.22 to 0.05) when readers set their own pace (full text) ([Delgado et al. 2018](https://doi.org/10.1016/j.edurev.2018.09.003)). A second meta-analysis, of 33 randomised experiments, found g = -0.25 overall and -0.32 for expository text. It found no difference in reading time and better judgement of one's own performance on paper (g = 0.20) (abstract) ([Clinton-Lisell 2019](https://doi.org/10.1111/1467-9817.12269)).

A later experiment (Delgado and Salmerón 2021) had 140 recruited participants, 132 analysed, reading one 3,010-word text. With free time, paper and screen did not differ (67.3% against 68.2% comprehension). Mind-wandering was the same on both (0.22), so it does not explain a gap there. The study did not measure fatigue (full text) ([Delgado and Salmerón 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC7463273)). What causes the timed-reading gap is not settled.

No source measured how page length, density or scrolling changes fatigue or return rate. Pages of 18,000 words (see section 4) are outside anything the reading literature covers.

### 2.4 Why people stop

Dropout from self-study is common and front-loaded. In three university MOOCs, clustering found four patterns (completing, auditing, disengaging, sampling). Disengaging learners usually dropped within the first third of the course. Shares varied: sampling about 39% in one course and 80% in another. This was observational, among people who chose to enrol (full text) ([Kizilcec et al. 2013](https://web.stanford.edu/~cpiech/bio/papers/deconstructingDisengagement.pdf)). Stated reasons across reviews were time, motivation, background knowledge and not understanding the content, not the look of the material (summary only, not rechecked) ([Frontiers in Education 2022](https://www.frontiersin.org/articles/10.3389/feduc.2022.1074435)).

Interest theory says surface novelty can trigger interest, but keeping it depends on knowledge growth and personal value (abstract and summaries only, not rechecked) ([Hidi and Renninger 2006](https://works.swarthmore.edu/fac-education/12)). Curiosity rises with a gap between what you know and what you want to know. In a trivia study, higher curiosity went with better recall 1-2 weeks later (summary only, not rechecked; student volunteers, trivia, not documents) ([Kang et al. 2009](https://www.cmu.edu/dietrich/sds/docs/loewenstein/WickCandleLearning.pdf)).

Habit work suggests a stable cue helps. In Lally et al., 96 volunteers each chose an eating, drinking or activity behaviour and did it daily in the same context for 84 days. 82 gave enough data. A habit curve could be fitted for 62, and fitted well for 39. The modelled time to reach 95% of the person's own ceiling ranged from 18 to 254 days, so some estimates run well past the 84 days observed. The widely quoted figure of 66 days is not in the abstract. Secondary sources call it a median, and the university interview calls it an average. This was not confirmed in the paper text, which could not be reached (abstract) ([Lally et al. 2010](https://doi.org/10.1002/ejsp.674)). The behaviours were not reading. It supports a consistent time and place to open the pages more than a consistent look.

### 2.5 Active versus passive

This is where the evidence is strongest. All figures below come from students and lab or class material, not adults learning skills from video notes.

Testing beats restudying. Across 159 effect sizes from 61 studies, testing versus restudy gave g = 0.50 overall (CI 0.42 to 0.58). It was g = 0.69 when the final test came at least 1 day later and 0.41 under 1 day. With feedback it was 0.73. Without feedback it was 0.39. When the first attempt scored 50% or less with no feedback, there was no reliable benefit (g = 0.03, CI -0.21 to 0.27) (full text) ([Rowland 2014](https://doi.org/10.1037/a0037559)). In the classic experiment on prose passages, restudy won at a 5-minute test, and testing won at 2 days and 1 week, even though restudying left students more confident (abstract) ([Roediger and Karpicke 2006](https://doi.org/10.1111/j.1467-9280.2006.01693.x)).

In real classrooms the effect is smaller but present. 222 studies, 48,478 students: overall g = 0.499. Versus restudying it was 0.330. Versus no or filler activity it was 0.610. Versus other active strategies (note-taking, summarising, concept mapping; 6 effects) it was 0.095, CI 0.005 to 0.194, p = .062, so not clearly different. Feedback gave 0.537 against 0.374 without. In continuing-education classes it was 0.314 and not significant (p = .119), from 6 effects that all came from one study (full text) ([Yang et al. 2021](https://doi.org/10.1037/bul0000309)). The earlier meta-analysis by Adesope et al. (2017) found practice tests better than restudying and all other comparison conditions (abstract). Its numbers are known here only through Yang et al.: g = 0.51 against restudying, and no feedback effect (0.63 with, 0.60 without). That conflicts with Rowland on feedback. The conflict is not resolved.

Transfer to doing is weaker. Testing gave transfer d = 0.40, CI 0.31 to 0.50, across 192 effects from 122 experiments in 67 articles (N = 10,382). It was greatest across test formats and to application and inference questions, and weakest to untested material and to worked-example problems. After correcting for publication bias, the predicted transfer often fell to none unless the practice used elaborated retrieval, response congruency or good initial performance (full text) ([Pan and Rickard 2018](https://doi.org/10.1037/bul0000151)). A recall quiz alone should not be assumed to train doing.

Spacing helps retention. Cepeda et al. found 839 assessments in 317 experiments from 184 articles, all on verbal recall. In the spaced-versus-massed comparison itself (271 comparisons from 254 studies), spaced study scored 47.3% against 36.7% for massed. Spaced was ahead at every retention interval, but the gap was statistically clear only for the two shortest intervals (under 10 minutes) and for 8-30 days (p = .05). The bins from 10 minutes to 7 days had 9 to 15 comparisons each and were not significant. 229 of the 271 comparisons tested within 10 minutes, and one tested at 31 days or more. The best gap grew with the delay: gaps under a minute for tests under a minute away, and gaps of at least a month for tests six months or more away. Expanding gaps either helped or did no better than fixed gaps (full text) ([Cepeda et al. 2006](https://doi.org/10.1037/0033-2909.132.3.354)). So the direction is well supported. The size at days to weeks, which is where a page revisit sits, is thinly supported.

The Dunlosky et al. review rated practice testing and distributed practice as high utility, and rated rereading, highlighting and summarising as low (full text) ([Dunlosky et al. 2013](https://doi.org/10.1177/1529100612453266)).

Self-explanation prompts gave g = 0.55 over 69 effect sizes from 64 reports (abstract) ([Bisra et al. 2018](https://doi.org/10.1007/s10648-018-9434-x)). Worked examples gave g = 0.48 on maths performance (abstract per the report, not rechecked) ([Barbieri et al. 2023](https://link.springer.com/content/pdf/10.1007/s10648-023-09745-1.pdf)). Prequestions help when the answers are shown afterwards, with no pooled size (abstract) ([Pan and Carpenter 2023](https://doi.org/10.1007/s10648-023-09814-5)).

Learners misjudge this. Easy re-reading feels better and tests worse. In Kornell and Bjork's painting-style experiments (adults, induction of an artist's style), 85% of participants did at least as well with spaced study as with massed, so at most 15% did better massed. Yet 83% rated massed study as equal or better. The figures combine two experiments (full text) ([Kornell and Bjork 2008](https://doi.org/10.1111/j.1467-9280.2008.02127.x)). The owner's sense that a polished page was "learned" is therefore not evidence.

Variation that changes what the learner does has support. A review of over 150 studies found more variable input slows early learning but gives more general performance, and it is about varying examples, not layout (summary only, not rechecked) ([Raviv et al. 2022](https://forms.mpi.nl/node/54558)). Interleaving gave g = 0.42 across 59 studies (238 effects), on practice items. It was best for paintings (0.67) and small for maths (0.34). Effects for expository texts were not significant, and blocking beat interleaving for words (g = -0.39) (abstract of the author manuscript) ([Brunmair and Richter 2019](https://www.psychologie.uni-wuerzburg.de/fileadmin/06020400/2019/Brunmair_Richter_in_press__2019_META-ANALYSIS_OF_INTERLEAVED_LEARNING.pdf)). Notes pages are mostly expository, so do not assume interleaving carries over.

## 3. Prior art

### 3.1 Products

Mechanisms that keep products worth reopening are few and repeat. Products offer several output formats from one source (NotebookLM lists notes, audio, video, mind maps, reports, flashcards, quizzes, slides and more) ([NotebookLM Help](https://support.google.com/notebooklm/answer/16206563)). Almost all add a quiz or flashcard layer. Several resurface old items on a schedule: Readwise decays an item's chance of reappearing each time it is shown, and its Mastery feature models recall with a half-life ([Readwise docs](https://docs.readwise.io/readwise/docs/faqs/reviewing-highlights)). Recall builds a knowledge graph and quizzes on a spaced schedule ([Recall](https://www.recall.it/)). Duolingo uses streaks. Pure summarisers vary nothing and have no review loop (reviews, secondary only). I found no product that restyles the same page type over time. The variety found is in output type. The NotebookLM, Readwise and Recall pages were not rechecked in this pass.

Published evidence is thin.

- Learn Your Way (Google Research) is the most relevant. 60 high-school students aged 15 to 18, one 90-minute session, one topic, a neuroscience chapter. Immediate recall was 77% against 68% (p = .029). Recall 3-7 days later was 78% against 67% (p = .03). 58 of 60 completed the later test. The control was a plain digital textbook without quizzes or feedback, so gains may come from interactivity, not from the format. Every user of the tool used its quiz feature. Of 30 tool users, 17 used slides, 14 mind maps, 6 audio and 4 video. More formats did not significantly predict scores (r = .24, p = .206 immediately), though the direction was positive and n was 30. Google funded the study and took part in its design, collection and analysis. I found no journal version. The arXiv v2 is dated 2026-03-26 and v1 had a different title ([arXiv 2509.18664](https://arxiv.org/abs/2509.18664)).
- Duolingo's streak A/B tests (company-run, blog post dated 2020-11-19) measured return behaviour. Day-14 retention rose 3.3% (relative) when the daily goal was split from the streak. That compares two streak designs, not streaks against none ([Duolingo blog](https://blog.duolingo.com/improving-the-streak)). A 2026 eight-week observational case study found the app drives retention without building habits that persist without it (abstract only, not rechecked) ([WR Publishing](https://www.wr-publishing.org/index.php/ijmat/article/view/908)).
- No controlled study of Readwise review was found. One critic argues resurfacing controls timing, not recall ([Matuschak notes](https://notes.andymatuschak.org/zAt1K9ARQYguinoHH8cfaqQ)).
- Khanmigo's founder reportedly said many students did not use it (secondary report of an interview, original not read) ([Ground News](https://ground.news/article/khan-academys-founder-says-ai-tutoring-revolution-hasnt-come-for-education-yet)). A good optional tool nobody opens is the same failure as page fatigue.
- Features with no learning evidence found: audio and video overviews, mind maps, infographics, knowledge graphs, summaries, social highlights. This is "none found", not "shown not to work".

Not verified from primary pages: ChatGPT study mode, Anthropic's learning mode, Mindgrasp, NoteGPT, Eightify, Otter, Notta, Glarity, Matter, Heptabase, Logseq.

### 3.2 Open-source sweep, 2026-11-08

Window: repositories created 2026-05-08 to 2026-11-08, plus all-time incumbents. Sources: GitHub search via script and `gh api`, Hacker News, the MCP registry, npm and PyPI, an FSRS list, and a benchmark page. Stars and dates are from 2026-11-08. Nothing was installed or run. In the fact check, the repository facts for the first three rows and the scheduler rows below were rechecked with `gh api` and the READMEs.

Our page today: one fixed design per video, diagram type chosen by content, an optional one-time quiz, no scheduling, no flashcard export, no link between pages.

**Full fits: none.** One project, take-notes, covers the first half of the job: video in, designed HTML page out. Its README claims no check of the notes against the source and has no review loop. No project does all of: video in, designed page out, checked against the source, and keeps the page worth reopening. (The report said no project does video in and designed page out. That was wrong. See the first row.)

Partial fits:

| Piece | Project | What it offers | Limits |
|---|---|---|---|
| Video in, designed page out; layout varied by source type | davertor/take-notes (MIT, 20 stars, created 2026-08-14, last push 2026-10-01, v1.6.0) | One self-contained HTML note from a video, article, paper, deck or repo. Three bundled genres (offprint, fieldguide, recipe) plus your own. Nine named colour themes plus an automatic one. Markdown export and an Anki export built from key points and concepts. | Very new. The README claims no source check and no review loop, and does not mention Windows. No claims measured. The README says the composition never changes between themes. |
| Page that resurfaces | wangsoft/ELI5 (MIT, 6 stars, created 2026-08-26) | One HTML page per concept with quiz, explain-back, flashcards and a local ledger of when each item is due. A point missed twice leads to the section being rewritten. The page is made only when the user asks for one. | Three commits and the last push all fall inside 40 minutes on 2026-08-26. Unproven. |
| Fact-check gate | analyticalmonk/explain-this (MIT, 22 stars, created 2026-05-04, last push 2026-10-26) | A gate skill: every checkable claim traced to a source, corrected, or cut. Interactive explainers from papers, posts or transcripts. | Not built for video. No claims measured. |
| Fill-in-blank notes | Polaris-Aeterna/loom-notes (177 stars, licence not recognised by GitHub) | Fill-in blanks and "your turn" tasks | PDF via TeX, not HTML; stars in a burst |
| Review schedule | lowwwbank/anything-to-course (MIT, 34 stars) | Hidden answers, checkpoints, review file | Markdown only |
| Resurfacing loop | ProjectAJ14/eklavya (MIT, 29 stars) | Due reviews in a dashboard; page rebuilt from missed items | Code-focused; sends usage counts |
| Scheduler | `fsrs` on PyPI (MIT, v6.3.2; repository open-spaced-repetition/py-fsrs, 526 stars); `ts-fsrs` on npm (MIT, 860 stars) | Pure-Python or JS scheduler | Evidence is from Anki review histories only |
| Card export | genanki (MIT, 2,798 stars, last push 2024-12-30); hashcards (Apache-2.0, 1,188 stars) | Write `.apkg` offline, or plain-text cards with FSRS | genanki slow-maintained; hashcards Windows unchecked |
| Linking | claude-obsidian, llm_wiki, course2md | Vault or library of linked notes | General, not study-specific |

The loom-notes, anything-to-course and eklavya rows were checked only for existence, stars, dates and licence, not for their READMEs. The hashcards and linking rows were not rechecked.

FSRS was measured on Anki review histories. The benchmark README reports 9,999 collections and 349,923,850 evaluation reviews. Its dataset section also keeps a struck-through older description (20 thousand users, 1.7 billion reviews) beside the newer one (10 thousand users, 727 million reviews), so it is inconsistent about dataset size. In its table without same-day reviews, log loss was 0.3370 for the FSRS-7 "recency" variant (plain FSRS-7: 0.3401), 0.3460 for FSRS-6, 0.3726 for FSRS v4, and 0.3945 for AVG, which predicts each user's constant average retention (lower is better). A moving-average predictor with no memory model scored 0.3369, about level with FSRS-7 recency. The result covers flashcards reviewed regularly, not a page that may or may not be reopened. The benchmark repository has no licence file.

Matuschak's essay on a "situated idea memory system" (essay, HN, 2026-11-06) argues fixed cards become cues to pattern-match, and proposes review tasks varied over time and generated from the source context. It has no released code. It is the argument for why generated material goes stale. Not rechecked.

Not a fit: large human-written note collections, Telegram "video note" bots, language-card generators, thin quiz-wrapper repos, hosted quiz MCP servers, Obsidian-only plugins, and whole apps that replace the product (NitroAI, studiamo, studyai, engram).

**Gaps line for the sweep.** The GitHub all-time incumbent search hit an HTTP 403 rate limit on several wordings because six runs went in parallel. Reruns one at a time worked for "spaced repetition", "lecture notes" and "learning page"; the rest returned nothing above a 150-star display cut-off, so a quiet result is not proof nothing exists. In-window repositories under 5 stars were not read. READMEs were skimmed, not run. Hugging Face hits were junk. GitHunt, OSS Insight and skills.sh returned no usable list. Product Hunt, AlternativeTo, Reddit, Lobsters, Smithery and LMArena were not tried. Organisations passed: readwiseio, open-spaced-repetition, ankitects, google. Not checked as organisations: Obsidian, RemNote, Logseq. The take-notes miss in the original summary shows the skim could understate a project: its README was only skimmed the first time.

## 4. Our own evidence: the 13 baseline pages measured

This section was not rechecked in the fact check. It reports local measurements.

Method: each page was parsed by script and measured in a browser at 1280x800. Only geometry and text were measured. No screenshots were taken, no phone view was measured, and no one was asked how the pages feel. Words are visible words in the main column, including collapsed quiz answers. Reading time uses 230 words per minute.

**The pages grew.** Runs 1-7 average 6,130 words (about 20 to 40 minutes). Runs 8-13 average 11,247 words (22 to 81 minutes). Runs 12 and 13 are about 18,000 words (77 and 81 minutes, 87 to 106 screens). The longest page is 3.8 times the shortest (run 3, 4,620 words). Pixels per word fell from about 5.8-7.0 in runs 1-6 to 3.8-4.9 in runs 7-13, because screenshots were cut back. Recent pages are denser text, not only longer.

**The skeleton is the same on all 13.** Every page opens with the same four blocks (hero, video details, "what you'll be able to do", "what the video teaches"), then 4 to 10 parts that each open with an "In 30 seconds" recap, then a cheat sheet and a glossary. The first real topic section starts 3.3 to 6.2 screens down, after 445 to 986 words. The details table has identical row labels on all 13, and the "Rating" row reads "Not rated yet" on every page.

**The prose does not repeat.** Only 0.70% of pooled words (762 of 109,543) sit in blocks that appear on 5 or more pages, and all are labels. Average 5-gram overlap between page pairs is 0.0006 (Jaccard). The sameness is in structure, labels and look, not in sentences. A text-similarity check would call the pages unique, which would miss what the owner is describing.

**The look has stopped changing.** All 13 use the same three fonts, the same sticky-rail layout and the same dark-mode scheme. Runs 6 and 8-13 share one ten-colour accent set. Adjacent runs from 8 to 13 share 0.96 to 0.97 of CSS declarations, and runs 9 and 11 have byte-identical stylesheets. Since run 8 the changes have been in length and in whether a quiz exists.

**Little of the page is active.** Nine of 13 pages (runs 1-7, 9, 11) have nothing the reader can do beyond zooming a screenshot. Four pages (runs 8, 10, 12, 13) carry a five-part, 20-question self-test with hidden answers and remembered ticks. That is 7% to 17% of those pages' words (answers included). The first quiz sits 7.4 to 15.1 screens down. Between quizzes there are 2 to 39 screens of passive reading. No page has a free-text input, an exercise, or a "try it" step. The recap boxes are summary, not activity.

**What was not measured:** whether the owner scrolls, ticks the quiz boxes, or reopens any page; whether quiz items repeat the recap bullets; whether the pages are correct or doable. The evidence on the page itself is about form only.

## 5. What this implies

### 5.1 Changes with learning evidence

These are the changes the literature supports. Each effect is stated with what it was measured on.

1. **Put an attempt before the answer.** A prompt to recall or predict, then reveal. Basis: testing versus restudy g = 0.50 (lab, students, passages and word lists) and g = 0.499 overall in classes (222 studies). It is larger after a day or more and larger with feedback. The cheat sheet already supplies feedback. The missing part is the reader producing an answer first.
2. **Keep every question answerable, or show the answer straight after.** First attempts at 50% or less with no feedback gave no reliable benefit (Rowland 2014, g = 0.03).
3. **Space the retrieval over days.** Spacing beat massing overall in 254 comparisons on verbal recall (Cepeda 2006). It was clearly significant at very short delays and at 8-30 days, and not significant in the few comparisons from 10 minutes to 7 days. Do not assume the size at days, or that it works for practical skills. The cost is a return visit, which is where adherence is likely to fail.
4. **For "do what it teaches" pages, add a completion step.** Remove a step or two from a worked example and ask the reader to fill them in, then a full attempt later. Basis is worked examples g = 0.48 in maths (abstract, not rechecked) and self-explanation g = 0.55. Nothing was found for adults learning software or hands-on skills from video-derived notes. Recall testing transfers weakly to worked-example problems, so recall questions alone will not train doing.
5. **Vary the question, not the skin.** A "teach it back" prompt, a fill-in, a predict-the-next-step. Rowland and Adesope appear to disagree on the best question format (this is Yang's description; Adesope's own numbers were not reached), and matching the practice format to the final task helped (g = 0.531 versus 0.399, Yang 2021). This is the only variety with a learning route, and no study tested it on note pages. Interleaving evidence does not carry over to expository text (not significant in Brunmair and Richter 2019).
6. **Keep the structural cues; trim redundant frame.** Signalling has support (Schneider 2018: retention g = 0.53, transfer 0.33, mostly short lab lessons). Expertise reversal suggests that boilerplate a regular reader no longer needs is cost, not help. The "Rating: Not rated yet" row on all 13 pages is an example of a block that carries nothing.
7. **Make the pages correct, complete and doable.** This is the owner's target, not evidence. Evidence is silent on whether a notes page can replace the video for doing. The watch-moment log is how to find out.
8. **Do not trust the feeling of learning.** Re-reading and polished pages feel effective and test worse (Roediger and Karpicke 2006, abstract; Kornell and Bjork 2008). Judge the pages by what the owner can do, not by how the page feels.

### 5.2 Changes that only add novelty

Novelty may bring the owner back once. None of it has learning evidence, and some has evidence of harm.

- A new colour theme, typeface or layout per page. No study; decoration unrelated to content hurts (g about -0.33, unverified summary), and a stable frame is the condition for the isolation effect.
- Audio, video, mind-map or infographic re-skins. In the one study touching them, 6 of 30 used audio, 4 of 30 video, and the number of formats did not significantly predict scores (n = 30, so the study could not detect a small effect).
- Streaks and daily notifications. Company A/B tests raised return rate. They measured return, not learning, and a 2026 case study found no habit left after removal. They treat "not opening" and leave the cause.
- Passive resurfacing of whole pages without a recall step. No controlled evidence; one critic says it controls timing, not recall.
- Genre-specific layouts (a recipe layout, a field-guide layout). These are plausible and cheap to try, and take-notes ships three, but the only support is that the pages differ, not that learning improves. Treat as a test candidate (section 6), not as a fix.

One caution in the other direction: some variety may help return visits without helping learning. The owner said they expect to tire of the same look. That is a stated expectation, not a measurement. It may be right, and the habit and MOOC evidence suggests the likelier cause of not opening is cost against return (time, length, relevance), not look. A length cap and a short entry point fit that cause better than a restyle.

## 6. Candidate tests the owner could run

The owner's target is notes that are correct, complete and doable, plus a one-line watch-moment log after each real use (did I open the video, where, why). The tests below use the lowest-budget methods: a closed-book quiz with and without the notes (hand-graded sample), hands-on replay, and a small human comprehension test. The human test is the only one that observes learning directly.

Use pages that already exist. Runs 9 and 11 share a stylesheet with runs 8, 10, 12 and 13 but have no quiz, which gives a natural contrast. Do not compare long and short pages across different videos and call the difference a design effect.

**Test A. Attempt-first versus read-only (retrieval step).**
- Compare: the same page read as is, versus the same page with 5 "try before you look" prompts at the start of each part, answers hidden below.
- Material and length: two baseline videos, one per condition, then swap the conditions on two other videos. Four pages in total, read over about two weeks.
- Judge: a closed-book quiz of 10 short questions per page, taken 1 day and 7 days after reading. Leave out questions the owner could answer before reading the page. Hand-grade a sample against the notes. Compare the 7-day scores, and note minutes spent per page. Both conditions are the same owner, so treat the result as one person's pattern and expect noise.

**Test B. Doable-from-the-page replay.**
- Compare: do the task a video teaches using only the page, with no video.
- Material and length: two to three videos that teach a hands-on task, one session each.
- Judge: did the task get done; log each watch moment (did I open the video, at what point, why). A moment where the video was needed marks a gap in the page's correctness, completeness or doability. This directly tests the owner's target. It does not test whether the page stays worth opening.

**Test C. Return-visit test with a due ledger.**
- Compare: one page with a due-date ledger and explain-back (the open-source ELI5 approach) versus the same page with none.
- Material and length: one baseline video's notes, 7 days.
- Judge: count unprompted reopenings on due dates. Set the bar before starting (for example, reopened on at least 3 of the due dates); no source gives one. If the owner does not return, scheduling will not rescue the page.

**Test D. Layout by source type.**
- Compare: our page versus a genre-contract layout (from take-notes) built from the same transcript.
- Material and length: one baseline video, one sitting each.
- Judge: which page the owner would reopen, plus the same 10-question closed-book quiz on each at 7 days. Preference alone is not learning evidence, so the quiz is the check.

**Test E. Fill-in blanks versus checklist.**
- Compare: the "Test yourself" checklist versus 10 hidden fill-in blanks on the same page.
- Material and length: one baseline page that already has the checklist (runs 8, 10, 12 or 13), one week.
- Judge: how many items are completed, and the owner's closed-book score at 7 days on a fresh set of questions.

**Test F. Human comprehension test.**
- Compare: pages versus the video, or pages versus no material.
- Material and length: a few videos, a small number of volunteer readers, one sitting plus a delayed check.
- Judge: comprehension questions and a short task. This is the only method that observes learning directly. It costs more than A to E.

**Recommended first test: Test A, with the watch-moment log kept throughout.** It targets the one change with the strongest evidence, uses pages that already exist, takes about two weeks, and can be judged by a hand-graded 7-day quiz. The log costs one line per use and gives Test B data for free. Run Test B second on whichever page the log flags most. Leave Tests C to E until A and B show the page content is sound, because a reopen test on a page that fails the doability check measures the wrong thing.

## 7. Sources table

"Read" shows how this fact check read the source. Entries marked "not rechecked" keep the report's reading status.

| Source | Measured on (population, material, outcome, delay) | How read | Limits |
|---|---|---|---|
| [Rowland 2014](https://doi.org/10.1037/a0037559) | 159 effects, 61 studies, mostly lab, testing versus restudy; delays under 1 day to over 1 day | Full text | Lab; students; word lists and passages |
| [Yang et al. 2021](https://doi.org/10.1037/bul0000309) | 222 studies, 48,478 students, real classes; exam scores | Full text | Continuing-education effect from 6 effects, one study; against active strategies p = .062 |
| [Pan and Rickard 2018](https://doi.org/10.1037/bul0000151) | 192 effects, 122 experiments, 67 articles, N = 10,382; transfer after testing | Full text | After bias correction, transfer often vanished without elaborated retrieval or good first performance |
| [Cepeda et al. 2006](https://doi.org/10.1037/0033-2909.132.3.354) | 839 assessments, 317 experiments, 184 articles; verbal recall; 271 spaced-vs-massed comparisons, 229 of them within 10 minutes | Full text | Mostly minutes; one comparison at 31 days or more; verbal items; middle bins not significant |
| [Dunlosky et al. 2013](https://doi.org/10.1177/1529100612453266) | Review of ten techniques; utility ratings | Full text | Ratings are the authors' judgement; mostly students |
| [Adesope et al. 2017](https://doi.org/10.3102/0034654316689306) | Practice testing meta-analysis | Abstract (no numbers); numbers via Yang et al. | Paywalled; numbers are second-hand |
| [Bisra et al. 2018](https://doi.org/10.1007/s10648-018-9434-x) | 69 effects, 64 reports; self-explanation prompts | Abstract | Instructor-scripted prompts; subgroup claims not verified |
| [Barbieri et al. 2023](https://link.springer.com/content/pdf/10.1007/s10648-023-09745-1.pdf) | Worked examples, maths performance | Abstract (not rechecked) | Maths; prompt-moderator result unclear |
| [Pan and Carpenter 2023](https://doi.org/10.1007/s10648-023-09814-5) | Prequestions, text, video and lectures | Abstract | No pooled size |
| [Roediger and Karpicke 2006](https://doi.org/10.1111/j.1467-9280.2006.01693.x) | Students, prose passages; tests at 5 min, 2 days, 1 week | Abstract | Design details beyond the abstract not read |
| [Kornell and Bjork 2008](https://doi.org/10.1111/j.1467-9280.2008.02127.x) | Adult lab participants, painting styles; induction | Full text | Lab; one task; figures combine two experiments |
| [Schneider et al. 2018](https://doi.org/10.1016/j.edurev.2017.11.001) | Signalling; 103 studies, 12,201 participants; mostly short lab lessons | Clearinghouse summary of the paper (abstract paywalled) | Second-hand; most tests immediate |
| [Richter et al. 2016](https://doi.org/10.1016/j.edurev.2015.12.003) | Signalling of text-picture links; 27 studies, 45 comparisons, N = 2,464 | Abstract | Replaces the wrong link in the report |
| [Kalyuga 2007](https://www.uky.edu/~gmswan3/EDC608/Kalyuga2007_Article_ExpertiseReversalEffectAndItsI.pdf) | Expertise reversal review | Summary only (not rechecked) | Reversals often partial; mostly structured tasks |
| [Sundararajan and Adesope 2020](https://doi.org/10.1007/s10648-020-09522-4) | Seductive details; 58 studies, over 7,500 students; cognitive outcomes; sessions mostly 6-12 minutes | Abstract and university press release | **g about -0.33 is an unverified summary**; no motivation outcomes |
| [Brom et al. 2018](https://artemis.ms.mff.cuni.cz/main/papers/emodesign_manuscript_1rev_180928_FINAL_norev.pdf) | 33 samples, N = 2,924; faces and colour on graphics; sessions up to about 30 min | Full text (author manuscript) | Short sessions; self-report afterwards; novelty could not be tested |
| [Hunt 1995](https://link.springer.com/content/pdf/10.3758/bf03197149.pdf) | Isolation effect; word lists | Summary only (not rechecked) | No meta-analysis; not tested on documents |
| [Delgado et al. 2018](https://doi.org/10.1016/j.edurev.2018.09.003) | 54 comparisons, 171,055 participants; reading on paper versus digital | Full text | Self-paced gap not significant; no fatigue outcome |
| [Clinton-Lisell 2019](https://doi.org/10.1111/1467-9817.12269) | 33 randomised studies, n = 2,799; paper versus screens | Abstract | Abstract only; no fatigue outcome |
| [Delgado and Salmerón 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC7463273) | 140 recruited, 132 analysed; one 3,010-word text; paper versus desktop | Full text (read through a page tool) | One text; desktop only; fatigue not measured |
| [Kizilcec et al. 2013](https://web.stanford.edu/~cpiech/bio/papers/deconstructingDisengagement.pdf) | Three university MOOCs; engagement patterns | Full text | Observational; enrolled learners; no causes |
| [Frontiers in Education 2022](https://www.frontiersin.org/articles/10.3389/feduc.2022.1074435) | Dropout reasons, MOOC reviews | Summary only (not rechecked) | Self-report; structured courses |
| [Hidi and Renninger 2006](https://works.swarthmore.edu/fac-education/12) | Four-phase interest model | Abstract and summaries (not rechecked) | Details of maintaining phase 2 not verified |
| [Kang et al. 2009](https://www.cmu.edu/dietrich/sds/docs/loewenstein/WickCandleLearning.pdf) | Student volunteers, trivia, fMRI and recall 1-2 weeks | Summary only (not rechecked) | Trivia, not documents |
| [Lally et al. 2010](https://doi.org/10.1002/ejsp.674) | 96 volunteers, 84 days; eating, drinking, activity; modelled for 62, good fit for 39 | Abstract (paper blocked) | Not reading; modelled range 18-254 days; 66-day figure unconfirmed |
| [Lally interview, Surrey](https://www.surrey.ac.uk/news/does-it-really-take-66-days-form-habit-we-asked-expert-dr-pippa-lally) | Interview about the study | Not rechecked | Secondary |
| [Raviv et al. 2022](https://forms.mpi.nl/node/54558) | Review of over 150 studies; variability | Summary only (not rechecked) | Not a meta-analysis; examples, not layout |
| [Brunmair and Richter 2019](https://www.psychologie.uni-wuerzburg.de/fileadmin/06020400/2019/Brunmair_Richter_in_press__2019_META-ANALYSIS_OF_INTERLEAVED_LEARNING.pdf) | 59 studies, 238 effects; interleaving practice items | Abstract of author manuscript | Practice items, not document format; not significant for expository text |
| [Xie et al. 2018 / critique 2020](https://link.springer.com/article/10.1007/s10648-020-09579-1) | 25 studies on perceptual disfluency; recall and transfer | Summary only (not rechecked) | Coding errors found in the original |
| [NotebookLM Help](https://support.google.com/notebooklm/answer/16206563) | Feature list | Full page (not rechecked) | Vendor page; no outcomes |
| [Readwise docs](https://docs.readwise.io/readwise/docs/faqs/reviewing-highlights) | Daily Review and Mastery design | Full page (not rechecked) | Vendor page; no outcome claims |
| [Recall](https://www.recall.it/) | Feature list; user counts | Full page (not rechecked) | Self-reported; no study |
| [Learn Your Way, arXiv 2509.18664](https://arxiv.org/abs/2509.18664) | 60 high-school students; one 90-min session; recall immediate and at 3-7 days | Full text, v2 | Control lacked quizzes and feedback; Google-funded and involved; n = 30 per arm; no journal version found |
| [Duolingo blog](https://blog.duolingo.com/improving-the-streak) | Company A/B test of splitting daily goal from streak; return rate; relative changes | Full page | Company-run; return, not learning; not streaks against none |
| [WR Publishing 2026](https://www.wr-publishing.org/index.php/ijmat/article/view/908) | Eight-week observational case study, one app | Abstract only (not rechecked) | One app; observational |
| [Matuschak notes](https://notes.andymatuschak.org/zAt1K9ARQYguinoHH8cfaqQ) | Expert critique of resurfacing | Page read (not rechecked) | Opinion |
| [Ground News on Khanmigo](https://ground.news/article/khan-academys-founder-says-ai-tutoring-revolution-hasnt-come-for-education-yet) | Report of an interview | Summary only (not rechecked) | Secondary; original not read |
| take-notes, ELI5, explain-this (GitHub) | Repositories; licence, dates, README claims | `gh api` and READMEs, 2026-11-08 | READMEs read, nothing run |
| open-spaced-repetition repositories, `fsrs` on PyPI, srs-benchmark README | Scheduler packages; benchmark on Anki review histories | `gh api`, PyPI, README | Benchmark covers regular flashcard review only |
| Open-source sweep, 2026-11-08 (GitHub, `gh api`, registries) | Repositories and package pages | READMEs skimmed; nothing run | See the gaps line in section 3.2 |
| Baseline pages, runs 1-13 | 13 generated pages; structure, text, CSS, geometry | Parsed by script; browser geometry at 1280x800 (not rechecked) | No readers, no screenshots, no phone view |

## 8. Gaps and limits of this research

- No study tests a fixed versus varied document template over weeks, with return use or learning as the outcome. The central question has no direct evidence. Sections 2.1 to 2.3 are inference from neighbouring work.
- No evidence on adults learning practical skills from video or from notes made from video. All effect sizes come from students on passages, word lists or class content. The one adult-workshop number (g = 0.314) is not significant and rests on 6 effects from one study.
- No evidence on the use of personal, self-generated study notes, and no source on habit formation for reading or learning material. MOOC and health-habit data stand in.
- Some effect sizes are still second-hand or unreached: the seductive-details size (g about -0.33), the Adesope numbers, Schneider's numbers (clearinghouse summary), the interleaving and disfluency claims beyond abstracts, and the 66-day habit figure. Check them in the primary papers before quoting them outside this file.
- No evidence on how page length (up to 18,000 words here), density or scrolling affects fatigue or return rate. The screen-versus-paper cost is small and tied to timed reading.
- Product evidence is mostly company-run or marketing. Primary pages for several products were unreadable or never reached (listed in section 3.1), and the product pages that were read were not reread in the fact check. Product-level resurfacing has no controlled evidence.
- Sweep limits: one rate-limited channel, small repositories skipped, nothing run, and several channels returned no list (see section 3.2). All sweep projects are weeks to months old and have no measured results, so none is shown to work.
- Baseline measurement describes form only. It cannot show whether pages are correct, complete or doable, and it observed no reader.
- The owner's target (correct, complete, doable, plus a watch-moment log) is a decision, not a finding. Nothing here shows that it will keep the pages worth opening. It does give a way to find out.
- A single reader (n = 1) cannot be answered from the literature. Any test here gives one person's pattern, not a general result.

## 9. Comparison with what we already have (stage 2)

Written after sections 1-8 were committed (814560c), from the issue's "Stage 2: what we already have" comment. Upstream links in it were checked on 2026-11-08 with `gh`.

### 9.1 The ideas, one by one

| Idea (from the comment) | What the evidence says | Verdict |
|---|---|---|
| 1. Vary the look per video (theme or accent from topic or thumbnail) | No study shows a changing skin helps learning or return. Decoration unrelated to content lowers learning (2.2). Purposeful design gains were measured only in sessions of 30 minutes or less. A stable frame is what makes a changed element stand out (2.1). No product found restyles the same page type over time (3.1). | **Novelty only.** Harmless if it stays an accent colour and adds no decoration, but it should not be counted as a fix. |
| 2. Vary the page's shape by kind of video (lab, argument map, decision grid, chapter index) | Found independently: take-notes ships this as "genres" (3.2). The parts that change what the reader *does* have support: a tutorial as a lab with steps to carry out fits worked examples and completion (5.1, item 4) and the owner's "doable" target. The parts that only change layout have none. Argument maps were not researched here (gap). | **Partly supported.** Keep the active half (the lab), test the layout half (Test D) before building it. |
| 3. Shorter and skimmable (30-second version and cheat sheet first, folded parts, skim mode) | The measured pages back the concern: runs 12-13 are about 18,000 words (77-81 minutes), and the first topic starts 3-6 screens down (section 4). Dropout studies point to time and cost, not look (2.4). But two parts conflict with the evidence: leading with the answers (cheat sheet, summary) removes the chance to retrieve first (2.5), and summarising and re-reading are rated low utility (Dunlosky 2013). A skim mode risks the feeling of learning without the learning (Kornell and Bjork 2008). No source measured length against return rate. | **Supported for length; wrong for order.** Cut length and the preamble; put the cheat sheet last for lookup on revisits, not first on first read. |
| 4. Make pages active (quiz first, fill-in lines, flashcard export, "do it" checklist) | The strongest evidence in this file (2.5). "Quiz first" is prequestions or pretesting, which helps when answers are shown afterwards. Fill-in lines are generation and completion. Flashcard export only pays if the owner returns, which is where adherence fails. A "do it" checklist matches the "doable" target, and recall quizzes alone transfer weakly to doing. | **Supported, and wider than the working view.** Retrieval helped facts (g 0.52), concepts (0.64) and application (0.45) in classes (Yang 2021), so it belongs on every page, not only skill videos. |
| 5. Keep the navigation fixed; vary only the content area | Signalling supports stable structural cues (2.1). A stable frame is the condition for the isolation effect. Habit work favours a stable cue for when and where, not a stable look (2.4). | **Supported** (indirectly). |
| 6. Measure before deciding (skipped or abandoned parts, watch-moment log) | Agrees with section 6. One gap: the watch-moment log as defined in #29 records when the video had to be opened, which measures doability, not fatigue. It does not record a page that was never opened or abandoned partway. | **Supported; extend the log.** Add one line per page: opened it? stopped where? |

### 9.2 What we had that this research did not find

- **The upstream report** (QingYunA/answer-me-with-html#349, opened and closed 2026-10-29). One user, after about a week of heavy use, wrote that the pages' repeated structure made them tired and that freshness mattered most. It is one anecdote, about a different use (answers to questions, not study notes), and the cause is the user's own reading. It shows the fatigue happens. It does not show the cause is the look; the dropout evidence (2.4) points at cost and value first.
- **Archify** (tt-a1i/archify, Apache-2.0, created 2026-04-15, about 94,700 stars): interactive diagrams with focus, route tracing and presentation mode. The sweep missed it because it searched for study material, not diagram tools. No learning evidence was found for interactive diagrams. Route tracing could count as a generative activity only if it asks the reader to predict or trace before being shown; as a viewer it is presentation.
- **dsh-genui** (omdsh-dev/dsh-genui, MIT, created 2026-08-13): self-grading quizzes and draggable plots inline in chat. Its self-grading quiz is a working example of idea 4 with feedback. It runs only in one harness, so it is a reference, not a dependency.
- **The fork's Reply and Remark buttons.** Not found by this research. They are a cheap way to capture watch moments and abandoned parts inside the page, which serves idea 6.
- **The fork already has a self-test with show-answer boxes.** This meets the feedback condition in 2.5 (answers shown straight after the attempt).
- **The two cold readers on run 10.** Claim tags stacked three to a line and a counter repeated in every part felt heavy. This matches the expertise-reversal point (2.1): repeated furniture a reader no longer needs is cost. Goal 5 lacked a worked example, which matches 5.1 item 4 and the "doable" target. Two readers, one page, one sitting: a signal, not a measurement.

### 9.3 What this research found that we had missed

- **Spacing and the return visit.** None of the six ideas brings the owner back to an old page on a schedule. Spaced retrieval over days is the second-strongest finding (2.5), and the open-source pieces exist (FSRS as a scheduler, a due ledger as in ELI5, genanki for export) (3.2). Flashcard export alone does not schedule anything.
- **Conditions for retrieval to work.** Questions must be answerable or answered straight after; failed attempts without feedback gave no benefit (Rowland 2014). Varying the *question type* is the one variety with a learning route.
- **The feeling of tiring, or of liking a page, is not evidence of learning.** Any preference test needs a quiz beside it (Kornell and Bjork 2008; Roediger and Karpicke 2006).
- **Measured facts about our pages:** they grew 3.8 times from shortest to longest; 9 of 13 have nothing to do; the sameness is in skeleton, labels and look, not in sentences (0.7% repeated words), so a text-similarity check would miss it; the four-block preamble and the "Rating: Not rated yet" row repeat on every page and carry nothing on a revisit.
- **Prior art:** no product restyles the same page type; the variety offered is in *output type* (quiz, flashcards, audio, mind map). The only study of that (Learn Your Way) could not separate format from the quizzes, and students barely used audio or video.

### 9.4 Where the evidence says the working view is wrong

The working view was: 2 and 3 first, 4 for skill videos, 1 as polish, 5 always, 6 to choose.

- **4 should come first, and for every page.** It has the best evidence of any idea, for facts and concepts as well as skills.
- **3 is right about length and wrong about order.** Shorten, but don't lead with the answers.
- **2 is half novelty.** Its active half (a tutorial as a lab) has support; its layout half has none yet and should be a test, not a build.
- **1 is novelty only** and should not be weighed as a fix, even as polish.
- **5 and 6 stand.** 6 needs a line for unopened and abandoned pages.
- The upstream maintainer's request to name "a specific layout or theme" frames the fix as visual. The evidence doesn't support that framing.

Revised order from the evidence: **4 on every page (attempt first, answers straight after), then 3 (cut length and the preamble), with 5 always and 6 extended to record unopened pages. Test 2's layout half; treat 1 as optional.** The recommended first test (Test A, section 6) is unchanged.
