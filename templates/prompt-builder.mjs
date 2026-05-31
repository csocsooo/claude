// Összerakja a végső, MotionSites-stílusú hero promptot,
// amit átmásolhatsz Lovable / Bolt.new / v0 / Claude / Cursor felé.

import { styles } from './styles.mjs';
import { industries } from './industries.mjs';

export function buildPrompt({
  industryKey,
  styleKey,
  brandName,
  oneLiner,
  audience = 'modern teams',
  framework = 'react+tailwind',
  extras = [],
}) {
  const industry = industries[industryKey];
  const style = styles[styleKey];
  if (!industry) throw new Error(`Unknown industry: ${industryKey}. Try: ${Object.keys(industries).join(', ')}`);
  if (!style) throw new Error(`Unknown style: ${styleKey}. Try: ${Object.keys(styles).join(', ')}`);

  const frameworkLine = {
    'react+tailwind': 'React + TypeScript + Tailwind CSS. Use Framer Motion for entry animations. Single component named `Hero`.',
    'next': 'Next.js App Router + Tailwind CSS. Server component where possible, client component only for motion.',
    'html': 'A single, self-contained `index.html` file. Tailwind via CDN. Vanilla JS (no build step). All assets inline or via CDN.',
    'vue': 'Vue 3 SFC + Tailwind CSS. Use @vueuse/motion for transitions.',
  }[framework] || framework;

  const sections = [
    `# Hero Section: ${brandName}`,
    ``,
    `Build a single hero section for **${brandName}** — ${oneLiner}.`,
    `Industry context: ${industry.label}. Target audience: ${audience}.`,
    ``,
    `## Visual Direction — "${style.label}"`,
    `**Mood:** ${style.mood}`,
    ``,
    `**Color palette:**`,
    `- Background: ${style.palette.background}`,
    `- Surface: ${style.palette.surface}`,
    `- Text: ${style.palette.text}`,
    `- Accent: ${style.palette.accent}`,
    ``,
    `**Typography:**`,
    `- Display: ${style.typography.display}`,
    `- Body: ${style.typography.body}`,
    ``,
    `**Layout:** ${style.layout}`,
    ``,
    `## Motion & Interaction`,
    style.motion,
    ``,
    `## Copy`,
    `- Headline: write a single sentence using one of these formulas — ${industry.headlineFormulas.map((f) => `\`${f}\``).join(' / ')}. Make it about: ${oneLiner}.`,
    `- Subheadline (one sentence, max 18 words): ${industry.subheadlinePattern}`,
    `- Primary CTA: "${industry.ctas.primary}"`,
    `- Secondary CTA: "${industry.ctas.secondary}"`,
    `- Social proof: ${industry.socialProof}`,
    ``,
    `## Tech Requirements`,
    `- Framework: ${frameworkLine}`,
    `- Suggested libraries: ${style.libraries.join(', ')}`,
    `- Fully responsive (mobile breakpoint at 640px). On mobile: collapse asymmetric layouts to a single column, reduce display type to clamp(40px, 12vw, 72px), drop non-essential motion.`,
    `- Accessibility: WCAG AA contrast, prefers-reduced-motion respected (disable looping animations), all CTAs are real \`<button>\` or \`<a>\` with descriptive text.`,
    `- No lorem ipsum. No placeholder images — use CSS gradients, SVG, or shaders only.`,
    ``,
    `## Inspiration references`,
    style.inspiration.map((i) => `- ${i}`).join('\n'),
    ``,
    extras.length ? `## Additional notes\n${extras.map((e) => `- ${e}`).join('\n')}\n` : '',
    `## Output`,
    `Return only the production-ready code, no commentary. Component must look polished on first render — no \`/* TODO */\`, no empty handlers, no skeleton fallbacks. Treat this as the public homepage of a Series-A funded company.`,
  ];

  return sections.filter(Boolean).join('\n');
}

export function suggestStyleFor(industryKey) {
  const industry = industries[industryKey];
  if (!industry) return null;
  return industry.recommendedStyles;
}
