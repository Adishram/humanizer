#!/usr/bin/env python3
"""Micro-Stylometric and Wikipedia AI-Tell Auditor for adishram/humanizer.

Measures:
1. Sentence-length burstiness: SD (target >= 5.5 words) & CV (target >= 0.35) [Przystalski et al., 2025].
2. Left/mid-branching syntax ratio (target >= 0.25 non-SVO openings).
3. Zipf's law tail / Hapax legomena ratio (target >= 0.55 once-only words).
4. Punctuation Shannon entropy (target >= 1.25 bits across , . ; : ( ) ?).
5. POS bigram & nominalization proxies ('of the' chains, Latinate verbs).
6. Wikipedia 'Signs of AI writing' lexical and structural tells.
"""

import argparse
import json
import math
import re
import sys
from collections import Counter
from pathlib import Path

AI_VOCAB = {
    "delve", "delves", "delving", "tapestry", "intricate", "intricacies",
    "interplay", "pivotal", "underscores", "underscoring", "underscore",
    "testament", "vibrant", "nestled", "breathtaking", "groundbreaking",
    "renowned", "meticulous", "meticulously", "garner", "garnered",
    "bolster", "bolstered", "foster", "fostering", "showcase", "showcasing",
    "realm", "indelible", "transcends", "multifaceted", "synergy", "holistic"
}

LATINATE_VERBS = {
    "facilitate", "facilitates", "facilitated", "utilize", "utilizes", "utilized",
    "demonstrate", "demonstrates", "demonstrated", "implement", "implements",
    "implemented", "endeavor", "optimize", "optimizes", "optimized", "leverage",
    "leverages", "leveraged"
}

SUBORDINATE_STARTERS = {
    "when", "while", "although", "though", "because", "since", "unless", "until",
    "after", "before", "if", "once", "whether", "whenever", "wherever", "even",
    "despite", "under", "during", "inside", "without", "by", "from", "in", "on",
    "at", "for", "with", "but", "and", "so", "yet", "instead"
}


def audit_text(text: str) -> dict:
    cleaned = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    cleaned = re.sub(r"^\s*#.*$", "", cleaned, flags=re.MULTILINE)
    raw_sentences = [
        s.strip()
        for s in re.split(r'(?<=[.!?])\s+(?=[A-Z0-9"\'])', cleaned.strip())
        if len(s.split()) >= 2
    ]

    words = re.findall(r"\b[a-z']+\b", cleaned.lower())
    lengths = [len(re.findall(r"\b[a-zA-Z0-9']+\b", s)) for s in raw_sentences]
    n_sent = len(lengths)
    mean_len = sum(lengths) / n_sent if n_sent else 0.0
    variance = sum((l - mean_len) ** 2 for l in lengths) / n_sent if n_sent > 1 else 0.0
    sd_len = math.sqrt(variance)
    cv_len = sd_len / mean_len if mean_len > 0 else 0.0

    # Hapax legomena ratio
    counts = Counter(words)
    unique_count = len(counts)
    hapax_count = sum(1 for c in counts.values() if c == 1)
    hapax_ratio = hapax_count / unique_count if unique_count > 0 else 0.0

    # Non-SVO / Left-branching opening ratio
    non_svo = 0
    for s in raw_sentences:
        m = re.match(r'^["\']?([A-Za-z]+)', s)
        first_word = m.group(1).lower() if m else ""
        early_comma = bool(re.match(r"^[^,]{6,65},\s+[a-z]", s))
        if first_word in SUBORDINATE_STARTERS or early_comma:
            non_svo += 1
    non_svo_ratio = non_svo / n_sent if n_sent > 0 else 0.0

    # Punctuation Shannon entropy
    punct_marks = [",", ".", ";", ":", "(", "?"]
    p_counts = [cleaned.count(p) for p in punct_marks]
    total_p = sum(p_counts)
    punct_entropy = 0.0
    if total_p > 0:
        for c in p_counts:
            if c > 0:
                prob = c / total_p
                punct_entropy -= prob * math.log2(prob)

    # Tell patterns
    vocab_hits = [w for w in words if w in AI_VOCAB]
    latinate_hits = [w for w in words if w in LATINATE_VERBS]
    of_the_hits = len(re.findall(r"\bof the\b", cleaned, re.I))
    copula_hits = len(re.findall(r"\b(serves as|stands as|functions as|operates as|boasts a|boasts over|boasted)\b", cleaned, re.I))
    neg_hits = len(re.findall(r"\b(not only\b[^.?!]*?\bbut also|not just\b[^.?!]*?\bbut|not merely\b[^.?!]*?\bbut|it's not\b[^.?!]*?\bit's|it is not\b[^.?!]*?\bit is)\b", cleaned, re.I))
    ing_hits = len(re.findall(r",\s*(highlighting|underscoring|emphasizing|reflecting|symbolizing|contributing to|cultivating|fostering|encompassing|showcasing|ensuring)\b", cleaned, re.I))
    sig_hits = len(re.findall(r"\b(marking a pivotal|marked a pivotal|key turning point|evolving landscape|setting the stage for|enduring legacy|lasting legacy|continues to thrive|a testament to|plays a crucial role|plays a pivotal role|plays a vital role)\b", cleaned, re.I))
    trans_hits = len(re.findall(r"(?m)^(?:Furthermore|Moreover|Additionally|Consequently|Subsequently|In conclusion|Ultimately|Notably),\b", cleaned))
    em_dashes = cleaned.count("—") + cleaned.count("–") + len(re.findall(r"\s--\s", cleaned))

    score = 100
    if sd_len < 5.5 and n_sent >= 4:
        score -= round((5.5 - sd_len) * 5)
    if cv_len < 0.35 and n_sent >= 4:
        score -= round((0.35 - cv_len) * 40)
    if hapax_ratio < 0.55 and len(words) >= 80:
        score -= round((0.55 - hapax_ratio) * 40)
    if non_svo_ratio < 0.25 and n_sent >= 4:
        score -= round((0.25 - non_svo_ratio) * 30)
    if punct_entropy < 1.25 and total_p >= 8:
        score -= round((1.25 - punct_entropy) * 10)
    score -= len(vocab_hits) * 4
    score -= len(latinate_hits) * 2
    score -= (copula_hits + neg_hits + ing_hits + sig_hits) * 6
    score -= trans_hits * 4
    score -= min(em_dashes * 3, 15)
    score = max(0, min(100, score))

    return {
        "humanization_score": score,
        "sentence_count": n_sent,
        "word_count": len(words),
        "mean_sentence_length": round(mean_len, 2),
        "sentence_length_sd": round(sd_len, 2),
        "burstiness_cv": round(cv_len, 2),
        "min_sentence_length": min(lengths) if lengths else 0,
        "max_sentence_length": max(lengths) if lengths else 0,
        "hapax_legomena_ratio": round(hapax_ratio, 3),
        "non_svo_opening_ratio": round(non_svo_ratio, 3),
        "punctuation_entropy_bits": round(punct_entropy, 2),
        "of_the_nominalization_count": of_the_hits,
        "ai_vocabulary_hits": vocab_hits,
        "latinate_verb_hits": latinate_hits,
        "negative_parallelism_hits": neg_hits,
        "shallow_ing_rider_hits": ing_hits,
        "inflated_significance_hits": sig_hits,
        "copula_avoidance_hits": copula_hits,
        "mechanical_transition_hits": trans_hits,
        "em_dash_count": em_dashes,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit text for micro-stylometric & Wikipedia AI tells.")
    parser.add_argument("file", nargs="?", help="Path to file (stdin if omitted)")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    args = parser.parse_args()

    text = Path(args.file).read_text(encoding="utf-8") if args.file else sys.stdin.read()
    res = audit_text(text)
    if args.json:
        print(json.dumps(res, indent=2))
    else:
        print(f"Humanization Score       : {res['humanization_score']}/100")
        print(f"Sentence Length SD / CV  : {res['sentence_length_sd']} words / CV {res['burstiness_cv']} (Range: {res['min_sentence_length']}-{res['max_sentence_length']})")
        print(f"Hapax Legomena Ratio     : {res['hapax_legomena_ratio']} (Target >= 0.55)")
        print(f"Non-SVO Opening Ratio    : {res['non_svo_opening_ratio']} (Target >= 0.25)")
        print(f"Punctuation Entropy      : {res['punctuation_entropy_bits']} bits (Target >= 1.25)")
        print(f"Wikipedia AI Tells       : vocab={len(res['ai_vocabulary_hits'])}, neg_parallel={res['negative_parallelism_hits']}, ing_riders={res['shallow_ing_rider_hits']}, sig={res['inflated_significance_hits']}, copula={res['copula_avoidance_hits']}, dashes={res['em_dash_count']}")


if __name__ == "__main__":
    main()
