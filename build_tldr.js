#!/usr/bin/env node
// Regenerates tldr.md — the static, copy-pasteable snapshot of the whole book
// (same file order and separator that tldr.html uses at runtime).
// Run after editing any chapter:  node build_tldr.js
const fs = require('fs');
const path = require('path');

const files = [
  'introduction.md',
  'chapter_1.md',
  'chapter_2.md',
  'chapter_3.md',
  'chapter_4.md',
  'chapter_5.md',
  'chapter_6.md',
  'chapter_7.md',
  'conclusion.md',
  'appendix.md',
];

const root = __dirname;
const text = files
  .map((f) => fs.readFileSync(path.join(root, f), 'utf8').replace(/\r\n/g, '\n').trimEnd())
  .join('\n\n---\n\n') + '\n';

fs.writeFileSync(path.join(root, 'tldr.md'), text, 'utf8');
const words = text.replace(/[#*`_]/g, '').split(/\s+/).filter(Boolean).length;
console.log(`tldr.md written: ${files.length} files, ${words.toLocaleString()} words, ${text.length.toLocaleString()} chars`);
