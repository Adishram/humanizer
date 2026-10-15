#!/usr/bin/env node
/**
 * @adishram/humanizer CLI
 * Usage:
 *   npx github:adishram/humanizer install [--global]
 *   npx github:adishram/humanizer audit <file.txt>
 *   npx github:adishram/humanizer prompt
 */

import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT_DIR = path.resolve(__dirname, '..');

const AI_VOCAB = new Set([
  'delve', 'delves', 'delving', 'tapestry', 'intricate', 'intricacies',
  'interplay', 'pivotal', 'underscores', 'underscoring', 'underscore',
  'testament', 'vibrant', 'nestled', 'breathtaking', 'groundbreaking',
  'renowned', 'meticulous', 'meticulously', 'garner', 'garnered',
  'bolster', 'bolstered', 'foster', 'fostering', 'showcase', 'showcasing',
  'realm', 'indelible', 'transcends', 'multifaceted', 'synergy', 'holistic'
]);

const LATINATE_VERBS = new Set([
  'facilitate', 'facilitates', 'facilitated', 'utilize', 'utilizes', 'utilized',
  'demonstrate', 'demonstrates', 'demonstrated', 'implement', 'implements',
  'implemented', 'endeavor', 'optimize', 'optimizes', 'optimized', 'leverage',
  'leverages', 'leveraged'
]);

const SUBORDINATE_STARTERS = new Set([
  'when', 'while', 'although', 'though', 'because', 'since', 'unless', 'until',
  'after', 'before', 'if', 'once', 'whether', 'whenever', 'wherever', 'even',
  'despite', 'under', 'during', 'Inside', 'without', 'by', 'from', 'in', 'on',
  'at', 'for', 'with', 'but', 'and', 'so', 'yet'
]);

export function auditText(text) {
  const cleaned = text.replace(/```[\s\S]*?```/g, '').replace(/^\s*#.*$/gm, '');
  const rawSentences = cleaned
    .trim()
    .split(/(?<=[.!?])\s+(?=[A-Z0-9"'])/)
    .map(s => s.trim())
    .filter(s => s.split(/\s+/).length >= 2);

  const words = (cleaned.toLowerCase().match(/\b[a-z']+\b/g) || []);
  const lengths = rawSentences.map(s => (s.match(/\b[a-zA-Z0-9']+\b/g) || []).length);
  const nSent = lengths.length;
  const meanLen = nSent ? lengths.reduce((a, b) => a + b, 0) / nSent : 0;
  const variance = nSent > 1
    ? lengths.reduce((acc, l) => acc + Math.pow(l - meanLen, 2), 0) / nSent
    : 0;
  const sdLen = Math.sqrt(variance);
  const cvLen = meanLen > 0 ? sdLen / meanLen : 0;

  // Hapax legomena ratio (unique words occurring exactly once / total unique words)
  const freq = new Map();
  for (const w of words) freq.set(w, (freq.get(w) || 0) + 1);
  const uniqueCount = freq.size;
  let hapaxCount = 0;
  for (const count of freq.values()) {
    if (count === 1) hapaxCount++;
  }
  const hapaxRatio = uniqueCount > 0 ? hapaxCount / uniqueCount : 0;

  // Left-branching / non-SVO opening ratio
  let nonSvoOpenings = 0;
  for (const s of rawSentences) {
    const firstWord = (s.match(/^["']?([A-Za-z]+)/)?.[1] || '').toLowerCase();
    const hasEarlyComma = /^[^,]{6,65},\s+[a-z]/.test(s);
    if (SUBORDINATE_STARTERS.has(firstWord) || hasEarlyComma) {
      nonSvoOpenings++;
    }
  }
  const nonSvoRatio = nSent > 0 ? nonSvoOpenings / nSent : 0;

  // Punctuation entropy (Shannon entropy across , . ; : ( ) ? !)
  const punctMarks = [',', '.', ';', ':', '(', '?'];
  const punctCounts = punctMarks.map(p => {
    let c = 0;
    for (const ch of cleaned) if (ch === p) c++;
    return c;
  });
  const totalPunct = punctCounts.reduce((a, b) => a + b, 0);
  let punctEntropy = 0;
  if (totalPunct > 0) {
    for (const c of punctCounts) {
      if (c > 0) {
        const p = c / totalPunct;
        punctEntropy -= p * Math.log2(p);
      }
    }
  }

  // Tell detectors
  const vocabHits = words.filter(w => AI_VOCAB.has(w));
  const latinateHits = words.filter(w => LATINATE_VERBS.has(w));
  const ofTheHits = (cleaned.match(/\bof the\b/gi) || []).length;
  const copulaHits = (cleaned.match(/\b(serves as|stands as|functions as|operates as|boasts a|boasts over)\b/gi) || []).length;
  const negParallelHits = (cleaned.match(/\b(not only\b[^.?!]*?\bbut also|not just\b[^.?!]*?\bbut|not merely\b[^.?!]*?\bbut|it's not\b[^.?!]*?\bit's|it is not\b[^.?!]*?\bit is)\b/gi) || []).length;
  const ingRiderHits = (cleaned.match(/,\s*(highlighting|underscoring|emphasizing|reflecting|symbolizing|contributing to|cultivating|fostering|encompassing|showcasing|ensuring)\b/gi) || []).length;
  const sigHits = (cleaned.match(/\b(marking a pivotal|key turning point|evolving landscape|setting the stage for|enduring legacy|lasting legacy|continues to thrive|a testament to|plays a crucial role|plays a pivotal role|plays a vital role)\b/gi) || []).length;
  const transHits = (cleaned.match(/^(Furthermore|Moreover|Additionally|Consequently|Subsequently|In conclusion|Ultimately|Notably),/gm) || []).length;
  const emDashes = (cleaned.match(/[—–]|\s--\s/g) || []).length;

  let score = 100;
  if (sdLen < 5.5 && nSent >= 4) score -= Math.round((5.5 - sdLen) * 5);
  if (cvLen < 0.35 && nSent >= 4) score -= Math.round((0.35 - cvLen) * 40);
  if (hapaxRatio < 0.55 && words.length >= 80) score -= Math.round((0.55 - hapaxRatio) * 40);
  if (nonSvoRatio < 0.25 && nSent >= 4) score -= Math.round((0.25 - nonSvoRatio) * 30);
  if (punctEntropy < 1.25 && totalPunct >= 8) score -= Math.round((1.25 - punctEntropy) * 10);
  score -= vocabHits.length * 4;
  score -= latinateHits.length * 2;
  score -= (copulaHits + negParallelHits + ingRiderHits + sigHits) * 6;
  score -= transHits * 4;
  score -= Math.min(emDashes * 3, 15);
  score = Math.max(0, Math.min(100, score));

  return {
    humanization_score: score,
    sentence_count: nSent,
    word_count: words.length,
    mean_sentence_length: Number(meanLen.toFixed(2)),
    sentence_length_sd: Number(sdLen.toFixed(2)),
    burstiness_cv: Number(cvLen.toFixed(2)),
    hapax_legomena_ratio: Number(hapaxRatio.toFixed(3)),
    non_svo_opening_ratio: Number(nonSvoRatio.toFixed(3)),
    punctuation_entropy_bits: Number(punctEntropy.toFixed(2)),
    of_the_nominalization_count: ofTheHits,
    ai_vocabulary_hits: vocabHits,
    latinate_verb_hits: latinateHits,
    negative_parallelism_hits: negParallelHits,
    shallow_ing_rider_hits: ingRiderHits,
    inflated_significance_hits: sigHits,
    copula_avoidance_hits: copulaHits,
    mechanical_transition_hits: transHits,
    em_dash_count: emDashes
  };
}

const args = process.argv.slice(2);
const cmd = args[0] || 'help';

if (cmd === 'audit') {
  const filePath = args[1];
  const input = filePath ? fs.readFileSync(filePath, 'utf8') : fs.readFileSync(0, 'utf8');
  const res = auditText(input);
  console.log(JSON.stringify(res, null, 2));
} else if (cmd === 'install') {
  const isGlobal = args.includes('-g') || args.includes('--global');
  const base = isGlobal ? os.homedir() : process.cwd();
  const targets = [
    path.join(base, '.claude', 'skills', 'humanizer'),
    path.join(base, '.agents', 'skills', 'humanizer')
  ];
  for (const dest of targets) {
    fs.mkdirSync(dest, { recursive: true });
    fs.copyFileSync(path.join(ROOT_DIR, 'SKILL.md'), path.join(dest, 'SKILL.md'));
    console.log(`Installed SKILL.md -> ${path.join(dest, 'SKILL.md')}`);
  }
} else if (cmd === 'prompt') {
  console.log(fs.readFileSync(path.join(ROOT_DIR, 'SKILL.md'), 'utf8'));
} else {
  console.log(`@adishram/humanizer v2.0.0
Usage:
  npx skills add adishram/humanizer              Install via Vercel Agent Skills CLI
  npx github:adishram/humanizer install [-g]     Install directly to .claude/skills & .agents/skills
  npx github:adishram/humanizer audit <file>     Run micro-stylometric & Wikipedia AI-tell audit
  npx github:adishram/humanizer prompt           Print SKILL.md instructions to stdout`);
}
