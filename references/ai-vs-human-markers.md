# AI vs. Human Text Differentiation Reference

This reference synthesizes empirical findings from Wikipedia's **WikiProject AI Cleanup** ([Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)), stylometric machine-generated text research ([Przystalski et al., 2025](https://arxiv.org/html/2507.00838v2); [Zaitsu et al., 2025](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0335369)), and commercial AI detector methodologies ([QuillBot](https://quillbot.com/blog/ai-writing-tools/burstiness-and-perplexity/), [Pangram](https://www.pangram.com/blog/why-perplexity-and-burstiness-fail-to-detect-ai), [GPTZero](https://support.gptzero.me/articles/9585228410-how-do-i-interpret-burstiness-or-perplexity)).

## 1. Micro-Stylometric Signatures Used by AI Detectors

| Feature | LLM Signature | Human Baseline Target | Primary Research Source |
| :--- | :--- | :--- | :--- |
| **Sentence-Length Standard Deviation (Burstiness)** | $22.3 \pm 2.6$ words (GPT-4) / $23.1 \pm 2.8$ words (GPT-3.5) | $\ge 5.5$ words (`CV >= 0.35`) | [Przystalski et al., 2025](https://arxiv.org/html/2507.00838v2) |
| **Syntactic Branching Direction** | Right-branching SVO clauses with trailing `-ing` participles | $\ge 25\%$ left-branching (periodic) or mid-branching openings | [Zaitsu et al., 2025](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0335369) |
| **POS Bigrams & Nominalizations** | High density of `JJ-NN-IN-JJ-NN` and `"of the"` nominalizations | Active finite verbs and unpacked noun stacks | [Zaitsu et al., 2025](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0335369) |
| **Function-Word Unigrams & Contractions** | Uniform determiner rate; mechanical sentence-initial adverbs (*Furthermore,*) | Mixed stressed/unstressed contractions; pronoun/conjunction links | [Zaitsu et al., 2025](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0335369) |
| **Zipf's Law Tail (Hapax Legomena)** | Repetitive middle-tier Latinate verbs (*facilitate, utilize, implement*) | Hapax legomena ratio $\ge 0.55$ with Anglo-Saxon phrasal verbs | [Pangram, 2025](https://www.pangram.com/blog/why-perplexity-and-burstiness-fail-to-detect-ai) |
| **Punctuation Entropy** | Narrow punctuation fraction ($12.2\% \pm 2.3\%$); overuse of em-dashes | Shannon entropy $\ge 1.25$ bits across `, . ; : ( ) ?`; zero em-dashes | [Przystalski et al., 2025](https://arxiv.org/html/2507.00838v2) |
| **Paragraph Symmetry & RLHF Hedging** | Uniform 3–4 sentence paragraphs ending in diplomatic summary | Asymmetric paragraph lengths (1, 5, 2 sentences) ending on hard facts | [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) |
