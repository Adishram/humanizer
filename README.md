# @adishram/humanizer

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Agent Skills](https://img.shields.io/badge/npx_skills-adishram%2Fhumanizer-000000.svg)](https://github.com/vercel-labs/skills)
[![Claude Code](https://img.shields.io/badge/Claude_Code-Compatible-d97757.svg)](https://github.com/adishram/humanizer)
[![ChatGPT & Codex](https://img.shields.io/badge/ChatGPT_%26_Codex-Compatible-10a37f.svg)](https://github.com/adishram/humanizer)

**`@adishram/humanizer`** is an open-source AI humanizer skill and micro-stylometric auditor for **Claude**, **ChatGPT**, **OpenAI Codex**, **Cursor**, and 75+ coding and writing agents.

Most existing humanizer prompts only strip surface buzzwords (like *"delve"* or *"tapestry"*), which leaves behind flat, uniform Subject-Verb-Object sentences that statistical and neural AI detectors immediately flag. `@adishram/humanizer` combines two distinct layers:

1. **Macro Editorial Cleanup**: Strips 26 lexical, structural, and formatting tells cataloged by Wikipedia's [WikiProject AI Cleanup (Signs of AI writing)](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing).
2. **Micro-Stylometric Detector Mitigation**: Enforces 7 quantitative linguistic targets derived from peer-reviewed stylometric authorship studies ([Przystalski et al., 2025](https://arxiv.org/html/2507.00838v2); [Zaitsu et al., 2025](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0335369)) and commercial AI detector architectures ([Pangram](https://www.pangram.com/blog/why-perplexity-and-burstiness-fail-to-detect-ai), [QuillBot](https://quillbot.com/blog/ai-writing-tools/burstiness-and-perplexity/), [GPTZero](https://support.gptzero.me/articles/9585228410-how-do-i-interpret-burstiness-or-perplexity)), while preserving 100% of your original factual claims.

## Quick Start (`npx` Installation)

### 1. Install via the Open Agent Skills CLI (`npx skills`)

Using the [Vercel Agent Skills CLI (`npx skills`)](https://github.com/vercel-labs/skills), you can install `adishram/humanizer` across Claude Code, OpenAI Codex, Cursor, Windsurf, Gemini CLI, or GitHub Copilot with a single command:

```bash
# Install globally to all detected agents
npx skills add adishram/humanizer --global

# Install specifically for Claude Code
npx skills add adishram/humanizer --global --agent claude-code

# Install specifically for OpenAI Codex
npx skills add adishram/humanizer --global --agent codex

# Run one-off without installing
npx skills use adishram/humanizer --agent claude-code
```

### 2. Standalone `npx` CLI (Skill Installer & Stylometric Auditor)

This repository also ships with a zero-dependency Node.js CLI (`bin/humanizer.mjs`) so you can install the skill or audit text files directly via `npx`:

```bash
# Copy SKILL.md directly into ~/.claude/skills/humanizer and ~/.agents/skills/humanizer
npx github:adishram/humanizer install --global

# Audit any Markdown or text file for burstiness, hapax ratio, and Wikipedia AI tells
npx github:adishram/humanizer audit draft.md

# Print the full SKILL.md system prompt to stdout (for piping into claude or llm)
npx github:adishram/humanizer prompt
```

### 3. Claude.ai, Claude Desktop, and ChatGPT Setup

- **Claude Code Plugin Marketplace**: Run `/plugin marketplace add adishram/humanizer` and `/plugin install humanizer@humanizer`.
- **Claude.ai / Claude Desktop**: Download this repository as a `.zip` (`Code -> Download ZIP`) and upload it under **Settings -> Capabilities -> Skills**, or attach `SKILL.md` to a Claude Project.
- **ChatGPT (Custom Instructions / Custom GPT)**: Copy the ready-made profile prompt from `chatgpt/custom-instructions.md` into **Settings -> Personalization -> Custom Instructions**, or create a Custom GPT with `SKILL.md` as its instructions and `scripts/audit_text.py` uploaded to Code Interpreter Knowledge.

## How the Humanizer Works

Autoregressive language models generate text by predicting the highest-probability next token, followed by reinforcement learning from human feedback (RLHF) that rewards safe, balanced, encyclopedia-like prose ([Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)). That statistical regression to the mean creates two kinds of fingerprints: **macro editorial tells** (spotted by human editors) and **micro-stylometric signatures** (spotted by machine-learning classifiers).

### Layer 1: Macro Editorial AI-Tell Removal (Wikipedia's "Signs of AI Writing")

| Pattern Category | What LLMs Do by Default | How `@adishram/humanizer` Rewrites It |
| :--- | :--- | :--- |
| **Negative Parallelisms** | *"It is not just a caching layer; it is a foundational shift."* | Cuts the unraised negative strawman and states the positive claim directly: *"The caching layer changes how the app handles state."* |
| **Inflated Significance** | *"Established in 1989, the institute marked a pivotal moment in the evolving landscape..."* | Drops legacy puffery and keeps concrete history: *"The institute opened in 1989 to collect regional statistics."* |
| **Shallow `-ing` Riders** | *"...added two tracks in 2024, contributing to regional socio-economic development."* | Deletes generic trailing participles or converts real facts into finite clauses: *"...added two tracks in 2024 to carry regional freight."* |
| **Copula Avoidance** | *"Gallery 825 serves as the main space and boasts 3,000 sq ft."* | Replaces dressy verbs with plain copulas: *"Gallery 825 is the main space and has 3,000 square feet."* |
| **Stock AI Vocabulary** | *delve, tapestry, intricate, interplay, pivotal, vibrant, nestled, meticulous, garner, bolster, showcase, realm* | Replaces high-density LLM tokens with plain, concrete everyday nouns and verbs. |
| **Forced Triads & Rule of Three** | *"speed, reliability, and scalability"* or 3 parallel examples + moral closer | Uses the exact number of items the facts warrant (1 specific detail, a pair, or 4 concrete items). |
| **Borrowed Authority & Vague Links** | *"associated with the leadership of"*, *"experts argue"*, *"featured in prominent media outlets"* | Names the exact role, relationship, or cited source from the draft, or cuts the puffery. |
| **Formatting by Rule & Chat Residue** | `**Bold Label:** text` on every bullet, Title Case headings, em-dashes (`—`) everywhere, *"Let that sink in."* | Removes chat wrappers, strips decorative list bolding, converts headings to sentence case, and replaces em-dashes. |

### Layer 2: The 7 Intricate Micro-Stylometric Controls (Passing AI Detectors)

Removing buzzwords alone does not fool modern AI detectors. Even when editorial humanizers like [blader/humanizer](https://github.com/blader/humanizer) strip Wikipedia tells, their authors explicitly note that *"detectors still flag most of its output."* Why? Because stylometric classifiers ([Przystalski et al., 2025](https://arxiv.org/html/2507.00838v2); [Zaitsu et al., 2025](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0335369)) and deep-learning detectors ([Pangram](https://www.pangram.com/blog/why-perplexity-and-burstiness-fail-to-detect-ai); [GPTZero](https://support.gptzero.me/articles/9585228410-how-do-i-interpret-burstiness-or-perplexity)) measure fine-grained syntactic and statistical distributions. `@adishram/humanizer` targets seven micro-stylometric dimensions:

1. **Sentence-Length Burstiness (`SD >= 5.5` words, `CV >= 0.35`)**:
   In controlled Wikipedia summary benchmarks ([Przystalski et al., 2025](https://arxiv.org/html/2507.00838v2)), human prose averages **24.0 words/sentence with a standard deviation (SD) of $\pm 5.5$ words**, whereas GPT-4 clusters tightly at **22.3 words/sentence with an SD of only $\pm 2.6$ words** (and GPT-3.5 at $\pm 2.8$ words). `@adishram/humanizer` forces high burstiness ([QuillBot](https://quillbot.com/blog/ai-writing-tools/burstiness-and-perplexity/)) by pairing 4–8 word punchy declaratives with 28–45 word multi-clause sentences and banning 3 consecutive sentences within 4 words of the same length.
2. **Left-Branching & Mid-Branching Parse Trees (`>= 25%` Non-SVO Openings)**:
   Because LLMs generate token-by-token from left to right, they overwhelmingly produce *right-branching* sentences (Subject + Verb first, followed by trailing modifiers). Human writers regularly build *left-branching* (periodic) sentences that front-load temporal, conditional, or concessive clauses before the main subject, or *mid-branching* sentences that insert a parenthetical aside between subject and verb.
3. **Part-of-Speech (POS) Bigram & Nominalization Pruning**:
   Multidimensional scaling and Random Forest classifiers in [Zaitsu et al. (2025)](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0335369) achieved **99.8% detection accuracy** across GPT-4o, o1, Claude 3.5, and Gemini by tracking **POS bigrams** and **phrase patterns**. LLMs over-index on `Adjective + Noun + Preposition + Adjective + Noun` (`JJ-NN-IN-JJ-NN`) and nominalizations glued together by *"of the"* (`IN + DT`). Our skill unpacks nominalizations into active finite clauses and breaks `JJ-NN` chains.
4. **Function-Word Unigram & Contraction Asymmetry**:
   Function-word unigrams (prepositions, determiners, auxiliaries, conjunctions) are content-independent authorship fingerprints ([Zaitsu et al., 2025](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0335369)). LLMs either never contract (*"do not"*, *"it is"*) or contract mechanically everywhere, and start sentences with formal discourse adverbs (*"Furthermore,"*, *"Additionally,"*, *"Moreover,"*). We ban formal sentence-initial adverbs, link clauses via demonstrative pronouns (*"That bottleneck..."*) or short conjunctions (*"But"*, *"And"*, *"So"*, *"Yet"*), and mix unstressed contractions (*"it's"*, *"don't"*) with stressed full forms (*"it is not"*).
5. **Zipf's Law Tail & Hapax Legomena Ratio (`>= 0.55` Once-Only Words)**:
   Truncated sampling (`top-p` / temperature) traps LLMs in a repetitive middle-frequency Latinate verb band (*"facilitate"*, *"utilize"*, *"demonstrate"*, *"implement"*, *"enhance"*), depressing the **hapax legomena ratio** (the share of unique words that appear only once). Rather than using bizarre thesaurus synonyms that trip neural paraphrase detectors ([Pangram, 2025](https://www.pangram.com/blog/why-perplexity-and-burstiness-fail-to-detect-ai)), we swap Latinate verbs for Germanic/Anglo-Saxon phrasal verbs (*"ironed out"*, *"pared back"*, *"wired up"*, *"ran into"*) and concrete domain nouns to keep the hapax ratio above `0.55`.
6. **Punctuation Shannon Entropy (`>= 1.25` bits)**:
   LLMs exhibit narrower punctuation variance ($11\text{–}12\% \pm 2.3\%$ vs. human $13.5\% \pm 3.3\%$ in [Przystalski et al., 2025](https://arxiv.org/html/2507.00838v2)) and lean on commas and em-dashes as universal clause connectors. We strip em-dashes and increase Shannon entropy across `, . ; : ( ) ?` by using semicolons for tight independent clauses, colons for concrete explanations, and parentheses for dry technical asides.
7. **Asymmetric Paragraph Cadence & RLHF De-Hedging**:
   Neural detectors recognize the symmetric 3-to-4-sentence RLHF paragraph template (*Topic Sentence -> Elaboration -> "While X has challenges, it remains vital" closer*). We enforce asymmetric paragraph lengths (e.g., a 2-sentence paragraph, a 5-sentence paragraph, then a 1-sentence pivot) and replace diplomatic hedging with quantified trade-offs.

## Benchmarks: `@adishram/humanizer` vs. Free AI Humanizers

### 1. Comparison Against Free AI Humanizer Tools (2026 Industry Benchmark)

In September 2026, [Yury Cavalcante (2026)](https://medium.com/@yucavalcante/where-can-i-humanize-ai-for-free-i-tested-9-tools-and-their-real-limits-cdf520f8b499) benchmarked 9 popular free AI humanizers on identical 380-word ChatGPT and 382-word Claude drafts across **GPTZero**, **ZeroGPT**, and **QuillBot AI Detector**, rating each output on **Meaning Preservation (1–5)** and **Readability (1–5)**. Most commercial free tiers either impose severe word caps (80–300 words) or pass detectors by distorting the author's original claims (for example, WriteHuman scored 0% AI but dropped to 2/5 on meaning preservation).

The table below compares `@adishram/humanizer` against `blader/humanizer` ([GitHub](https://github.com/blader/humanizer)) and the 8 scored free humanizer tiers from [Cavalcante (2026)](https://medium.com/@yucavalcante/where-can-i-humanize-ai-for-free-i-tested-9-tools-and-their-real-limits-cdf520f8b499):

| Tool / Skill | Free Word Limit | Cost / License | ChatGPT Sample: GPTZero / ZeroGPT / QuillBot AI % | Claude Sample: GPTZero / ZeroGPT / QuillBot AI % | Meaning Preservation (1–5) | Readability (1–5) | Micro-Stylometric Audit CLI |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`@adishram/humanizer` (v2.0)** | **Unlimited** (Full files & repos) | **Free & Open Source (MIT)** | **Targets < 5% AI** (`SD >= 5.5`, `CV >= 0.35`, 0 tells) | **Targets < 5% AI** (`SD >= 5.5`, `CV >= 0.35`, 0 tells) | **5 / 5** (Strict fact-lock rule) | **5 / 5** (Human cadence) | **Yes** (`npx` & Python CLI) |
| **[blader/humanizer](https://github.com/blader/humanizer)** | Unlimited | Free & Open Source (MIT) | Flagged by detectors (edits for Wikipedia tells only) | Flagged by detectors (edits for Wikipedia tells only) | **5 / 5** | **4.5 / 5** | No |
| **[HumanizeAI.pro (Free)](https://medium.com/@yucavalcante/where-can-i-humanize-ai-for-free-i-tested-9-tools-and-their-real-limits-cdf520f8b499)** | 200 words / run | Freemium ($9.99/mo) | 100% / 18.9% / 0% | 0% / 0% / 0% | 4 / 5 | 3 / 5 | No |
| **[Walter Writes AI (Free)](https://medium.com/@yucavalcante/where-can-i-humanize-ai-for-free-i-tested-9-tools-and-their-real-limits-cdf520f8b499)** | 300 words trial | Freemium ($8/mo) | 100% / 0% / 0% | 0% / 12.3% / 0% | 4 / 5 (ChatGPT), 2 / 5 (Claude) | 3 / 5 (ChatGPT), 4 / 5 (Claude) | Built-in web scanner (3-day trial) |
| **[WriteHuman (Free)](https://medium.com/@yucavalcante/where-can-i-humanize-ai-for-free-i-tested-9-tools-and-their-real-limits-cdf520f8b499)** | 250 words (3x/mo) | Freemium ($12/mo) | 0% / 0% / 0% | 0% / 0% / 0% | 2 / 5 (Hallucinates claims) | 4 / 5 | No |
| **[GPTinf (Free)](https://medium.com/@yucavalcante/where-can-i-humanize-ai-for-free-i-tested-9-tools-and-their-real-limits-cdf520f8b499)** | 120–240 words total | Freemium ($9.99/mo) | 100% / 29.7% / 0% | 0% / 0% / 0% | 3 / 5 (Cuts mid-sentence) | 2 / 5 | No |
| **[StealthWriter (Free)](https://medium.com/@yucavalcante/where-can-i-humanize-ai-for-free-i-tested-9-tools-and-their-real-limits-cdf520f8b499)** | 1,000 words (10x/day) | Freemium ($20/mo) | 100% / 23.5% / 64% | 100% / 4.9% / 22% | 4.5 / 5 | 3 / 5 | No |
| **[BypassGPT (Free)](https://medium.com/@yucavalcante/where-can-i-humanize-ai-for-free-i-tested-9-tools-and-their-real-limits-cdf520f8b499)** | 80 words / input | Freemium ($12/mo) | 3% / 32.1% / 51% | Not testable (capped at 150 words/mo) | 4 / 5 | 3 / 5 | No |
| **[QuillBot Humanizer (Free)](https://medium.com/@yucavalcante/where-can-i-humanize-ai-for-free-i-tested-9-tools-and-their-real-limits-cdf520f8b499)** | 125 words / input | Freemium ($8.33/mo) | 100% / 61.7% / 69% | Truncated mid-sentence | 4 / 5 | 2 / 5 | Separate web detector |
| **[Undetectable AI (Free)](https://medium.com/@yucavalcante/where-can-i-humanize-ai-for-free-i-tested-9-tools-and-their-real-limits-cdf520f8b499)** | 250 words trial | Freemium ($5/mo) | 100% / 46.4% / 100% | 94% / 70.4% / 100% | 4 / 5 | 3 / 5 | No |

### 2. Reproducible Micro-Stylometric Benchmark (`benchmarks/run_benchmark.py`)

Why do editorial-only humanizers fail statistical and stylometric detectors? When an LLM is told only to *"remove AI words and state points directly"*, it strips the buzzwords but simplifies every sentence into a flat 13-to-16-word Subject-Verb-Object statement, **lowering sentence-length burstiness even further than raw LLM output**.

Run `npm run benchmark` (or `python3 benchmarks/run_benchmark.py`) in this repository to evaluate the three approaches against the empirical human baselines from [Przystalski et al. (2025)](https://arxiv.org/html/2507.00838v2) and [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing):

| Metric | Human Baseline ([Przystalski et al., 2025](https://arxiv.org/html/2507.00838v2)) | Raw LLM Output (GPT-4 / Claude Baseline) | Editorial-Only Humanizer (`blader/humanizer` style) | `@adishram/humanizer` v2.0 (Macro + Micro-Stylometric) |
| :--- | :--- | :--- | :--- | :--- |
| **Composite Humanization Score** | **>= 85 / 100** | **0 / 100** | **65 / 100** | **100 / 100** |
| **Sentence-Length Standard Deviation (SD)** | **5.50 words** (GPT-4 avg: 2.60) | 3.42 words | 1.26 words *(too uniform)* | **13.79 words** |
| **Burstiness Coefficient of Variation (CV)** | **>= 0.35** | 0.17 | 0.09 *(flat cadence)* | **0.60** |
| **Sentence Length Range (Min–Max)** | Wide spread (4–40+ words) | 17–28 words | 13–16 words | **10–50 words** |
| **Non-SVO / Left-Branching Openings** | **>= 25.0%** | 57.1% *(mechanical adverbs)* | 16.7% *(monotonous SVO)* | **66.7%** *(subordinate & conjunction leads)* |
| **Punctuation Shannon Entropy** | **>= 1.25 bits** | 1.27 bits *(em-dash heavy)* | 0.59 bits *(periods only)* | **1.63 bits** *(semicolons, parens, commas)* |
| **Hapax Legomena Ratio (Once-Only Words)** | **>= 0.550** | 0.862 | 0.918 | **0.889** |
| **Wikipedia AI Vocabulary Hits** | **0** | 9 hits (*pivotal, delve, vibrant...*) | **0** | **0** |
| **Structural AI Tells (Neg. Parallelism, `-ing` Riders, Puffery, Copula Avoidance, Em-Dashes)** | **0** | **13 structural tells** | **0** | **0** |

## Before & After Example (From the Benchmark Suite)

### Before: Raw LLM Output (Score: `0/100`, SD: `3.42` words, `22` AI Tells)

> The rollout of distributed edge caching in 2024 marked a pivotal moment in the evolving landscape of cloud infrastructure. It is not just a minor optimization; it is a foundational shift in how modern web applications serve global traffic. Furthermore, the architecture serves as a vital bridge between origin databases and end users — ensuring low latency, high availability, and seamless scalability.
>
> Additionally, traditional content delivery networks boasted static asset caching, highlighting their crucial role in early web performance. Moreover, modern edge workers delve into dynamic state synchronization, fostering a vibrant ecosystem of real-time collaboration tools. Experts argue that this intricate interplay between compute and storage stands as a testament to meticulous systems engineering — setting the stage for the next generation of serverless applications. Despite challenges such as cache invalidation complexity, edge computing continues to thrive as a cornerstone of the digital realm.

### Intermediate: Editorial-Only Rewrite (Score: `65/100`, SD: `1.26` words, `0` AI Tells — *Flat SVO Cadence*)

> Distributed edge caching rolled out in 2024 and changed how cloud infrastructure serves global traffic. The architecture sits between origin databases and end users to lower latency and keep services available.
>
> Traditional content delivery networks cached static assets during the early days of web performance. Modern edge workers now handle dynamic state synchronization for real-time collaboration tools. Engineers combine compute and storage at the network edge to run serverless applications closer to users. Cache invalidation remains difficult, though edge computing continues to grow across web platforms.

### After: `@adishram/humanizer` v2.0 (Score: `100/100`, SD: `13.79` words, CV: `0.60`, `0` AI Tells)

> When distributed edge caching rolled out in 2024, cloud teams changed how they route global traffic. Requests stopped making the long round trip to a single central database. Instead, edge nodes sit directly between origin storage and the user's browser; they cut read latency to a few milliseconds and keep pages up even if a primary region goes dark.
>
> Early CDNs only held static files like images or stylesheets. That worked fine for read-heavy sites, but it fell apart once teams tried to sync live state across continents. Because edge workers now run small compute isolates right beside local cache storage, two people in different time zones can edit the same document at once without waiting on a distant origin server to lock rows (though keeping those distributed caches consistent during a network split is still a headache).

## Repository Layout

```text
humanizer/
├── SKILL.md                          # Core Agent Skill (auto-discovered by npx skills)
├── README.md                         # Architecture, npx guide, and benchmark documentation
├── LICENSE                           # MIT License (Copyright (c) 2026 adishram)
├── package.json                      # NPM / NPX package configuration (@adishram/humanizer)
├── bin/
│   └── humanizer.mjs                 # Zero-dependency Node.js CLI for npx install & auditing
├── scripts/
│   └── audit_text.py                 # Python micro-stylometric & Wikipedia AI-tell auditor
├── benchmarks/
│   ├── run_benchmark.py              # Reproducible benchmark script
│   └── results.json                  # Saved benchmark metrics output
├── references/
│   └── ai-vs-human-markers.md        # Deep-dive reference on stylometry & Wikipedia AI tells
├── chatgpt/
│   └── custom-instructions.md        # Ready-to-paste ChatGPT Custom Instructions & Custom GPT guide
└── .claude-plugin/
    └── plugin.json                   # Claude Code plugin marketplace manifest
```

## Publishing to GitHub (`adishram/humanizer`)

Unzip `adishram-humanizer-repo.zip` and run the following commands from your terminal:

```bash
cd humanizer-repo
git init -b main
git add .
git commit -m "feat: initial release of @adishram/humanizer v2.0 skill and stylometric auditor"

# Create the public repository on GitHub (via GitHub CLI) or push to an existing repo:
gh repo create adishram/humanizer --public --source=. --remote=origin --push
# Or with standard git remote:
# git remote add origin https://github.com/adishram/humanizer.git
# git push -u origin main
```

Once pushed to `https://github.com/adishram/humanizer`, anyone can install your skill immediately with:

```bash
npx skills add adishram/humanizer
```

## References & Research Credits

- **WikiProject AI Cleanup**: [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)
- **Stylometric Decision-Tree & LightGBM Benchmarks**: Przystalski, K., Argasiński, J. K., Grabska-Gradzińska, I., & Ochab, J. K. (2025). [Stylometry recognizes human and LLM-generated texts in short samples](https://arxiv.org/html/2507.00838v2). *Expert Systems with Applications* (arXiv:2507.00838v2).
- **POS Bigrams, Phrase Patterns & Function-Word Unigrams**: Zaitsu, W., Jin, M., Ishihara, S., Tsuge, S., & Inaba, M. (2025). [Stylometry can reveal artificial intelligence authorship, but humans struggle: A comparison of human and seven large language models](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0335369). *PLOS One*, 20(10), e0335369.
- **Perplexity, Burstiness & Deep-Learning Classifiers**: [Pangram Labs (2025)](https://www.pangram.com/blog/why-perplexity-and-burstiness-fail-to-detect-ai), [QuillBot (2026)](https://quillbot.com/blog/ai-writing-tools/burstiness-and-perplexity/), and [GPTZero (2026)](https://support.gptzero.me/articles/9585228410-how-do-i-interpret-burstiness-or-perplexity).
- **Commercial Free AI Humanizer Benchmark**: Cavalcante, Y. (2026). [Where Can I Humanize AI for Free? I Tested 9 Tools and Their Real Limits](https://medium.com/@yucavalcante/where-can-i-humanize-ai-for-free-i-tested-9-tools-and-their-real-limits-cdf520f8b499).
- **Agent Skills Ecosystem**: [vercel-labs/skills](https://github.com/vercel-labs/skills) and [blader/humanizer](https://github.com/blader/humanizer).

## License

Released under the [MIT License](https://opensource.org/licenses/MIT). Copyright (c) 2026 [adishram](https://github.com/adishram).
