# Legal and terms for video handling

**This is not legal advice.** An AI research agent, not a lawyer, wrote it. Sources were read on 2026-10-30. Items marked *Inference* are the author's reading, not what a source says.

## What the skill does

yt-dlp downloads the video and captions on the user's machine ([SKILL.md](../../skills/video-notes/SKILL.md)). `cloud_frames.py` can upload the video to a private Kaggle dataset, and nothing in it removes the latest video or the script output from Kaggle afterwards. Screenshots go into a page that may be published. `bench/README.md` lists yt-dlp commands for named videos, and `bench/labels/` includes short on-screen text, such as a novelist's quoted line.

## YouTube

- **Terms of Service** ([effective 5 Jan 2022](https://www.youtube.com/t/terms?gl=IN&hl=en), old but still live, and the same for an India request). They bar downloading or reproducing Content unless the Service expressly authorises it or YouTube and, where applicable, the rights holders give written permission. They also bar circumventing features that restrict copying, and most automated access.
- **Authorised route:** [Premium offline viewing](https://support.google.com/youtube/answer/11977233?hl=en&co=GENIE.Platform%3DDesktop).
- **API policies** ([updated 2026-10-15](https://developers.google.com/youtube/terms/developer-policies)). III.E.1 bars API clients from downloading or storing audiovisual content without written approval, or enabling others to.
- *Inference:* the skill's scripts call yt-dlp, not the API, so these policies don't bind it directly, but they show YouTube's position.

## yt-dlp and legal actions

- **License:** repo and PyPI code is under the [Unlicense](https://raw.githubusercontent.com/yt-dlp/yt-dlp/master/LICENSE); bundled executables are [GPLv3+](https://github.com/yt-dlp/yt-dlp).
- **Stated position:** I found no statement on legality or terms in the README or [FAQ](https://github.com/yt-dlp/yt-dlp/wiki/FAQ). The project refuses services used mainly for piracy, and [DRM-only services](https://raw.githubusercontent.com/yt-dlp/yt-dlp/master/CONTRIBUTING.md). YouTube downloads [need a JavaScript runtime](https://github.com/yt-dlp/yt-dlp/wiki/EJS) to solve YouTube's challenges.
- **youtube-dl on GitHub, 2020:** the [RIAA notice](https://raw.githubusercontent.com/github/dmca/master/2020/10/2020-10-23-RIAA.md) claimed §1201(a)(2) and (b)(1) violations through YouTube's "rolling cipher", citing sample code naming three songs and a Hamburg ruling. [GitHub reinstated the project](https://github.blog/news-insights/policy-news-and-insights/standing-up-for-developers-youtube-dl-is-back/) on 16 Nov 2020 after a patch and new information that it did not circumvent.
- **Yout v. RIAA (US):** the [D. Conn. decision of 30 Sep 2022](https://storage.courtlistener.com/recap/gov.uscourts.ctd.141714/gov.uscourts.ctd.141714.61.0.pdf) dismissed the claim of a service built on youtube-dl. Yout had not plausibly pleaded that YouTube lacks an effective technological measure, or that it does not circumvent one. This was at the pleading stage. The [Second Circuit appeal](https://www.courtlistener.com/docket/66697744/yout-llc-v-recording-industry-association-of-america-inc/) was argued on 5 Feb 2024. The docket mirror, updated 27 Oct 2026, shows no opinion but may lag.
- **Uberspace (Germany):** the Hamburg appeal court ([5 U 54/23, 21 Nov 2024, per heise](https://heise.de/-10179284)) upheld liability for a host of youtube-dl.org, and said [average users should recognise circumvention](https://heise.de/-10181247) in MP3-style downloads.
- **India:** the Delhi High Court issued an [ex parte interim order blocking 18 sites](https://barandbench.com/news/litigation/delhi-high-court-orders-blocking-18-websites-download-audiovideo-youtube-other-platforms) and ruled in [Saregama v. En.ssyou.tube](https://www.livelawbiz.com/high-court/delhi-high-court/delhi-high-court-restrains-websites-enabling-illegal-downloads-of-saregama-indias-copyrighted-music-310306) (10 Nov 2025). [One report](https://www.medianama.com/2025/11/223-delhi-hc-blocks-stream-ripping-sites-saregama/) says the court relied on YouTube's terms. These target hosted ripping sites. I found no case against an individual note-taker or a wrapper like this skill.
- **Cox v. Sony (US, [25 Mar 2026](https://www.law.cornell.edu/supremecourt/text/24-171)):** contributory liability needs inducement, or a service tailored to infringement; knowledge alone is not enough. *Inference:* §1201(a)(2) has its own test, so this doesn't settle trafficking.

## Kaggle

- **Terms** ([effective 22 Jun 2025](https://www.kaggle.com/terms)). You warrant that you hold all rights necessary for what you contribute, and agree not to upload Content you don't own without the owner's consent or in a way that violates rights. Use must be personal and non-commercial. Kaggle receives a perpetual, irrevocable licence to operate the Services, and you indemnify it.
- **Acceptable use** ([AUP](https://www.kaggle.com/aup)). Uploading data that violates IP rights is a given example of a violation. Activity unrelated to ML data science, and circumvention tools, are listed as resource abuse.
- **Does private change anything?** Only who sees the data and the licence's scope. [Private means](https://www.kaggle.com/docs/datasets) you, your collaborators, and Kaggle for purposes consistent with its privacy policy. The warranty and upload rule apply to all contributions.
- *Inference:* downloading locally avoids the AUP's clause on reaching other Google products from Kaggle, but not the rights warranty. Frame extraction for notes may also fit "ML data science" poorly.

## Copyright exceptions and anti-circumvention

**United States**

- [§107](https://www.law.cornell.edu/uscode/text/17/107) weighs purpose, nature, amount and market effect, and [no amount is automatically safe](https://www.copyright.gov/fair-use/more-info.html). [§102(b)](https://www.law.cornell.edu/uscode/text/17/102) leaves ideas and methods unprotected. [§101](https://www.law.cornell.edu/uscode/text/17/101) lists abridgments and condensations as derivative works.
- [Sony](https://www.law.cornell.edu/supremecourt/text/464/417) held private noncommercial time-shifting fair. [Warhol](https://www.law.cornell.edu/supremecourt/text/21-869) weighs against uses that share the original's purpose and can substitute for it. [Hosseinzadeh v. Klein](https://www.copyright.gov/fair-use/summaries/hosseinzadeh-klein-sdny2017.pdf) found clips fair in a critique that did not substitute.
- [§1201(a)(1)](https://www.law.cornell.edu/uscode/text/17/1201) bars circumventing access controls; (a)(2) and (b)(1) bar offering such tools. Fair use remains a defence to infringement, but Yout cites authority that end users' fair use is no DMCA defence.
- Remedies: [$200–$2,500 per act](https://www.law.cornell.edu/uscode/text/17/1203). [Criminal liability](https://www.law.cornell.edu/uscode/text/17/1204) requires wilfulness and commercial or financial gain. [Exemptions](https://www.copyright.gov/title37/201/37cfr201-40.html) cover listed criticism and educational uses, not personal notes as such.

**India** (from third-party reproductions of the Act)

- [§14(d)](https://lawgist.in/copyright-act/14): the film right includes copying by a photograph of any image. *Inference:* if a video is a "film", screenshots fall within that right.
- [§52(1)(a)](https://lawgist.in/copyright-act/52): fair dealing with any work except a computer programme, for private or personal use including research, or criticism or review, including electronic storage for those purposes.
- [Rameshwari Photocopy](https://indiankanoon.org/doc/114459608/) (Delhi HC, 2016) measured the separate teaching exception, §52(1)(i), by educational purpose. I found no ruling on screenshots.
- [§65A](https://lawgist.in/copyright-act/65A): circumvention is an offence only "with the intention of infringing such rights", with up to two years and a fine. Purposes the Act doesn't prohibit are excepted, but a facilitator must keep records. [§63](https://lawgist.in/copyright-act/63) punishes knowing infringement or abetment.

## Who carries which exposure

*Inference throughout.*

| Actor | Terms | Circumvention | Copyright | Overall |
| --- | --- | --- | --- | --- |
| **One person, own notes** | Breach of YouTube's terms; Kaggle's warranty if uploading | US: open, turns on Yout. India: weak without intent to infringe | Low: strongest on Sony and §52(1)(a)(i) | Mostly contract and account risk. The Kaggle copy is the weak point |
| **Person publishing notes** | As above, plus public use | Same | Highest for screenshots and verbatim copying. Needs fair use, or review or criticism in India | Real, and falls on the publisher; takedowns likely come first |
| **The project** | Not a party to the download, though it instructs agents to do it | US: §1201(a)(2)/(b)(1) "offering" theory. Germany: accessory theory | Cox helps. Labels hold minimal text | Low likelihood, high disruption: a GitHub takedown is the realistic form |

The project's own words matter here. The README promises learning "without watching it", and SKILL.md demands every example in full. *Inference:* both read as market substitution, and could feed an inducement or "marketed for" argument. "YouTube blocks cloud machines" explains the local download, though the script doesn't bypass that block. The RIAA notice relied on sample code naming specific works, and `bench/README.md` has a similar shape.

## How comparable tools word this

- [cobalt](https://raw.githubusercontent.com/imputnet/cobalt/main/README.md) has an ethics section: the end user is responsible for what they download and how they use it.
- [youtube-dl](https://raw.githubusercontent.com/ytdl-org/youtube-dl/master/README.md) and yt-dlp state which sites they support, not what users may do.
- [Tube Archivist](https://raw.githubusercontent.com/tubearchivist/tubearchivist/master/README.md) and [LibreTube](https://raw.githubusercontent.com/libre-tube/LibreTube/master/README.md) have no legal notice on this.
- *Inference:* a notice sets expectations and shows intent, which matters after Cox, but it doesn't bind rights holders.

## What this means for the decision

*Inference; options, not advice.*

1. Add a notice saying what each step does, whose terms apply, and that the user decides.
2. Make Kaggle explicitly opt-in, say that private doesn't change the rights warranty, and delete the dataset and output after each run.
3. Make publishing a deliberate choice, with fewer, cropped screenshots and links back to the source.
4. Reword "without watching it" and the wording about YouTube's block.
5. Replace named yt-dlp commands in `bench/README.md` with a neutral list or openly licensed videos, and correct the README's claim that labels only describe.

**Questions for a lawyer**

1. Does automating yt-dlp make the project an offeror under §1201, or an accessory in Germany?
2. What changes for individuals and the project when the Second Circuit rules in Yout?
3. Do YouTube's terms bind logged-out use, and what remedy follows, in the US and India?
4. Is a copy on private cloud compute covered by fair use or §52(1)(a)(i), and can a user honestly give Kaggle's warranty?
5. Can public study notes with screenshots qualify under fair use or §52(1)(a)(ii)? Is a YouTube upload a "cinematograph film"?
6. Can §63 abetment or §65A(2)(a) record-keeping duties reach an open-source project's maintainers?

## What I couldn't verify

- India Code and copyright.gov.in didn't load. The statutory text comes from lawgist.in, lawx.in and Indian Kanoon, and §65A(2)(e) was garbled on both copies I read.
- The Hamburg judgment and Delhi orders were read only through press reports, which differ on whether Saregama relied on YouTube's terms.
- I read only part of the Rameshwari judgment, not its final order.
- Kaggle's Copyright Help Center and privacy policy were not reviewed.
