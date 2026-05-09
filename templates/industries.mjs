// Industry presets — minden iparághoz tartozik egy
// pozicionálási sablon (headline-formula, alcím, CTA-k, social-proof,
// és tipikus illeszkedő stílus-ajánlások).

export const industries = {
  saas: {
    label: 'SaaS / Productivity',
    headlineFormulas: [
      'The {category} tool built for {audience}.',
      '{verb} {object}. {benefit}.',
      'One workspace. Every {workflow}.',
    ],
    subheadlinePattern: 'Replace {oldThing} with a single, fast, modern {newThing}. Free for {tier}.',
    ctas: { primary: 'Start free', secondary: 'Watch 60s demo' },
    socialProof: 'logo strip: 6 customer logos in grayscale, "Trusted by teams at" prefix',
    recommendedStyles: ['saasGradient', 'glassmorphism'],
  },

  portfolio: {
    label: 'Designer / Developer Portfolio',
    headlineFormulas: [
      '{firstName} {lastName} — {role} crafting {discipline}.',
      'Designing {nounPlural} that {verb}.',
      'Independent {role}. Available {availability}.',
    ],
    subheadlinePattern: '{years} years building for {clientTypes}. Currently {currentFocus}.',
    ctas: { primary: 'See selected work', secondary: 'Get in touch' },
    socialProof: 'inline list of past clients separated by middle-dots',
    recommendedStyles: ['darkCosmic', 'boldEditorial'],
  },

  agency: {
    label: 'Creative / Design Agency',
    headlineFormulas: [
      'We design {nounPlural} for {audience}.',
      'A studio for {discipline}. Based in {city}.',
      'Brand. Product. Motion. — {tagline}.',
    ],
    subheadlinePattern: 'Partnered with {clientCount}+ teams from {regionList}. Currently booking {season}.',
    ctas: { primary: 'View case studies', secondary: 'Start a project' },
    socialProof: 'awards row: Awwwards, FWA, CSSDA badges',
    recommendedStyles: ['glassmorphism', 'boldEditorial', 'darkCosmic'],
  },

  ai: {
    label: 'AI Product / Model',
    headlineFormulas: [
      'The {modality} model that {capability}.',
      '{ProductName}: {one-line value-prop}.',
      'Run {modality} {action} in {speed}.',
    ],
    subheadlinePattern: 'State-of-the-art {benchmark}. {pricingHook}. Used by {customerCount} developers.',
    ctas: { primary: 'Try it free', secondary: 'Read the paper' },
    socialProof: 'compact benchmark bar (vs. GPT-4o, vs. Claude) with delta-green numbers',
    recommendedStyles: ['web3Neon', 'darkCosmic', 'saasGradient'],
  },

  web3: {
    label: 'Web3 / Crypto Protocol',
    headlineFormulas: [
      'The {layer} for {primitive}.',
      '{verb} {asset}. Onchain. Permissionless.',
      'A new standard for {category}.',
    ],
    subheadlinePattern: 'Live on {chains}. Audited by {auditors}. ${tvl}+ TVL.',
    ctas: { primary: 'Launch app', secondary: 'Read docs' },
    socialProof: 'grid of supported chain logos + audit firm logos',
    recommendedStyles: ['web3Neon', 'cryptoWealth'],
  },

  crypto: {
    label: 'Crypto / Trading / Wealth',
    headlineFormulas: [
      'Compound {asset}. While you sleep.',
      'The smartest way to hold {asset}.',
      '{rate}% APY on {asset}, paid daily.',
    ],
    subheadlinePattern: 'Non-custodial. Audited. Withdraw anytime. ${aum}+ assets under management.',
    ctas: { primary: 'Connect wallet', secondary: 'View vaults' },
    socialProof: 'live numbers: TVL, average APY, total payouts',
    recommendedStyles: ['cryptoWealth', 'web3Neon'],
  },

  videoBrand: {
    label: 'Brand Film / Studio Reel',
    headlineFormulas: [
      'We make {nounPlural} that move people.',
      '{StudioName} — {discipline} in {city}.',
      'Film. Motion. Sound.',
    ],
    subheadlinePattern: 'Recent work for {clientList}. Reel below.',
    ctas: { primary: 'Watch reel', secondary: 'Brief us' },
    socialProof: 'one-line client list',
    recommendedStyles: ['videoCinematic', 'boldEditorial'],
  },

  emailMarketing: {
    label: 'Email / Newsletter Tool',
    headlineFormulas: [
      'Email that feels {adjective}.',
      'The {tool} for {audience} who care about craft.',
      'Send better email. In half the time.',
    ],
    subheadlinePattern: 'Beautiful templates. Real-time previews. {priceHook}.',
    ctas: { primary: 'Start sending', secondary: 'See templates' },
    socialProof: 'avatars + count: "Loved by 12,400+ creators"',
    recommendedStyles: ['saasGradient', 'glassmorphism'],
  },

  automotive: {
    label: 'Automotive / EV',
    headlineFormulas: [
      'Built for {terrain}. Made for {emotion}.',
      'The {model} — {tagline}.',
      'Range. Performance. Silence.',
    ],
    subheadlinePattern: '{range} mi range. 0–60 in {accel}s. Reservations open.',
    ctas: { primary: 'Reserve yours', secondary: 'Configure' },
    socialProof: 'press logos + key specs strip',
    recommendedStyles: ['videoCinematic', 'boldEditorial'],
  },
};

export const listIndustries = () => Object.keys(industries);
