#!/usr/bin/env node
// MotionSites-stílusú hero prompt generátor.
//
// Példák:
//   node generator.mjs --industry saas --style saasGradient --name "Apex" --tagline "The CRM teams actually use"
//   node generator.mjs --list
//   node generator.mjs --industry portfolio --name "Lukáš Vondra" --tagline "designer & developer based in Prague"
//
// Kimenet: a kész prompt stdout-ra. Másold be Lovable / Bolt / v0 / Claude felé.

import { buildPrompt, suggestStyleFor } from './templates/prompt-builder.mjs';
import { listStyles, styles } from './templates/styles.mjs';
import { listIndustries, industries } from './templates/industries.mjs';

function parseArgs(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (!a.startsWith('--')) continue;
    const key = a.slice(2);
    const next = argv[i + 1];
    if (!next || next.startsWith('--')) {
      args[key] = true;
    } else {
      args[key] = next;
      i++;
    }
  }
  return args;
}

function printList() {
  console.log('\nIndustries:');
  for (const k of listIndustries()) {
    console.log(`  ${k.padEnd(18)} — ${industries[k].label}`);
  }
  console.log('\nStyles:');
  for (const k of listStyles()) {
    console.log(`  ${k.padEnd(18)} — ${styles[k].label}`);
  }
  console.log('\nUsage:');
  console.log('  node generator.mjs --industry <key> --style <key> --name "Brand" --tagline "one-liner"');
  console.log('  Optional: --audience "..." --framework react+tailwind|next|html|vue --extras "note1;note2"');
  console.log('  If --style omitted, the first recommended style for the industry is used.\n');
}

const args = parseArgs(process.argv.slice(2));

if (args.list || args.help || (!args.industry && !args.name)) {
  printList();
  process.exit(0);
}

const industryKey = args.industry;
if (!industries[industryKey]) {
  console.error(`Unknown industry: ${industryKey}`);
  printList();
  process.exit(1);
}

const styleKey = args.style || suggestStyleFor(industryKey)?.[0];
if (!styles[styleKey]) {
  console.error(`Unknown style: ${styleKey}`);
  printList();
  process.exit(1);
}

const brandName = args.name || 'Acme';
const oneLiner = args.tagline || 'a one-line description of what you do';
const audience = args.audience || 'modern teams';
const framework = args.framework || 'react+tailwind';
const extras = typeof args.extras === 'string' ? args.extras.split(';').map((s) => s.trim()).filter(Boolean) : [];

const prompt = buildPrompt({ industryKey, styleKey, brandName, oneLiner, audience, framework, extras });
process.stdout.write(prompt + '\n');
