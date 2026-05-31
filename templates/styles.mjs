// Visual style modules — minden style egy "esztétikai recept",
// ami a MotionSites prompt-könyvtár visszafejtett mintáit követi.
// Mindegyik stílus megadja: hangulat, paletta, tipográfia, layout,
// motion technika és az ajánlott JS könyvtárak.

export const styles = {
  glassmorphism: {
    label: 'Glassmorphism Agency',
    mood: 'premium, airy, soft-futuristic',
    palette: {
      background: 'soft gradient mesh from #f0f4ff to #e8e1ff with subtle noise',
      surface: 'frosted glass panels — backdrop-filter: blur(24px), 1px white/15% border',
      text: '#0a0e1f primary, #4a5172 secondary',
      accent: '#5b6cff electric indigo',
    },
    typography: {
      display: 'Inter Tight or Geist, weight 600, tracking -0.04em, size clamp(56px, 8vw, 128px)',
      body: 'Inter, weight 400, size 18px, line-height 1.5',
    },
    layout: 'centered hero with floating glass cards rotated -6deg / +6deg around the headline; pill-shaped CTA group below',
    motion: 'mouse-parallax on the floating cards (5–12px shift), gradient mesh slowly drifting via CSS @keyframes (40s loop), text fade+slide-up on load (stagger 60ms)',
    libraries: ['framer-motion', 'tailwindcss'],
    inspiration: ['linear.app', 'vercel.com', 'arc.net'],
  },

  darkCosmic: {
    label: 'Dark Cosmic Portfolio',
    mood: 'cinematic, mysterious, high-contrast',
    palette: {
      background: 'pure #05060a with animated radial gradient (deep purple #1a0b3d → transparent) following cursor',
      surface: 'transparent, separated by 1px #ffffff10 hairlines',
      text: '#f5f5f7 primary, #8a8a94 secondary',
      accent: '#c4f542 acid lime, used sparingly on hover only',
    },
    typography: {
      display: 'Editorial New or PP Editorial, weight 400 italic, size clamp(72px, 10vw, 180px), tracking -0.05em',
      body: 'JetBrains Mono, weight 400, size 14px, uppercase, letter-spacing 0.1em',
    },
    layout: 'asymmetric split: large editorial headline left (60%), vertical scrolling marquee of work tags right (40%); fixed top-left mark + top-right time/location badge',
    motion: 'on-load: scrambled text reveal (200ms per character); idle: vertical infinite marquee (30s loop); scroll: GSAP scroll-triggered horizontal pan to next section; cursor: custom dot follower',
    libraries: ['gsap', 'gsap/ScrollTrigger', 'split-type'],
    inspiration: ['igor.gold portfolio', 'olliepark.com', 'studio-okk.com'],
  },

  web3Neon: {
    label: 'Web3 Neon 3D',
    mood: 'futuristic, technical, energetic',
    palette: {
      background: '#0a0014 with 3D animated mesh (iridescent purple→cyan)',
      surface: 'thin 1px #ffffff20 outlined cards with neon glow on hover',
      text: '#ffffff primary, #b8b8d4 secondary',
      accent: '#00f0ff cyan + #ff2ec4 magenta gradient',
    },
    typography: {
      display: 'Space Grotesk, weight 700, tracking -0.03em, size clamp(64px, 9vw, 144px); secondary line in monospace',
      body: 'IBM Plex Mono, weight 400, size 15px',
    },
    layout: 'centered headline with rotating 3D torus knot / icosahedron behind it; CTA pill row + "trusted by" logo strip below; animated grid floor in foreground',
    motion: 'Three.js: continuously rotating low-poly geometry with iridescent shader; on-scroll camera dolly forward; headline characters glow-pulse in sync with mesh rotation',
    libraries: ['three', '@react-three/fiber', '@react-three/drei', 'framer-motion'],
    inspiration: ['arc.computer', 'replicate.com hero', 'midjourney homepage'],
  },

  boldEditorial: {
    label: 'Bold Editorial Portfolio',
    mood: 'confident, magazine-like, type-forward',
    palette: {
      background: '#fafaf7 warm off-white',
      surface: 'flat, no borders, generous whitespace',
      text: '#0c0c0c primary, #6b6b6b secondary',
      accent: '#ff4500 vermilion for hover and CTAs',
    },
    typography: {
      display: 'PP Neue Montreal or Söhne, weight 500, tracking -0.06em, size clamp(96px, 14vw, 240px) — fills viewport edge to edge',
      body: 'PP Neue Montreal Mono, weight 400, size 13px, uppercase',
    },
    layout: 'massive name/word fills the viewport; tiny meta info top-left and top-right corners; a single horizontal hairline divider with project count below',
    motion: 'text mask reveal on load (clip-path inset 100% → 0%, ease-out 1.2s); on hover of the headline, letters individually scale 1.02 with stagger; subtle grain overlay (CSS noise SVG) at 3% opacity',
    libraries: ['gsap', 'split-type'],
    inspiration: ['rauno.me', 'paco.me', 'rafa.gallery'],
  },

  saasGradient: {
    label: 'SaaS Aurora Gradient',
    mood: 'fresh, optimistic, conversion-focused',
    palette: {
      background: 'top-down aurora gradient: #6366f1 → #8b5cf6 → #ec4899 with grain texture',
      surface: 'white #ffffff cards with subtle shadow shadow-2xl',
      text: '#ffffff on hero, #0f172a inside cards',
      accent: '#fbbf24 amber for the primary CTA',
    },
    typography: {
      display: 'Geist or Inter, weight 700, tracking -0.04em, size clamp(48px, 6vw, 96px)',
      body: 'Geist, weight 400, size 18px, line-height 1.6',
    },
    layout: 'centered headline + subtitle + dual CTA (primary amber + ghost white) + screenshot/UI mockup below floating with perspective tilt',
    motion: 'gradient hue-rotates 8° over 12s; UI mockup floats up-down (4px, 6s ease-in-out); on scroll, mockup tilts back to flat; trust badges fade in with stagger',
    libraries: ['framer-motion', 'tailwindcss'],
    inspiration: ['linear.app', 'cron.com', 'raycast.com'],
  },

  cryptoWealth: {
    label: 'Crypto Wealth Hero',
    mood: 'luxurious, dark-gold, trustworthy',
    palette: {
      background: '#0a0a0a with gold-foil noise + animated candlestick chart silhouette',
      surface: 'matte black with #d4af37 gold hairlines',
      text: '#ffffff primary, #d4af37 accent gold',
      accent: '#d4af37 gold + #00ff88 profit-green for live numbers',
    },
    typography: {
      display: 'Fraunces or PP Editorial, weight 600, italic, size clamp(56px, 8vw, 128px)',
      body: 'Inter, weight 500, size 16px, tabular-nums for stats',
    },
    layout: 'split: serif editorial headline left, live ticker / animated number counters right (volume, market cap, APY); gold hairline divider; two CTAs',
    motion: 'numbers count up on viewport-enter (1.5s ease-out); ticker scrolls horizontally; gold particles drift slowly; chart silhouette breathes (scale 1 → 1.02)',
    libraries: ['framer-motion', 'react-countup', 'lightweight-charts'],
    inspiration: ['oxide.computer', 'mercury.com', 'rho.co'],
  },

  videoCinematic: {
    label: 'Video Cinematic Hero',
    mood: 'immersive, brand-film, atmospheric',
    palette: {
      background: 'fullscreen looping muted video (Mux HLS) with #00000080 dark overlay',
      surface: 'transparent, glass pill nav at top',
      text: '#ffffff with mix-blend-mode: difference',
      accent: '#ffffff with thin 1px outline buttons',
    },
    typography: {
      display: 'Söhne or Inter Display, weight 500, tracking -0.04em, size clamp(64px, 9vw, 160px)',
      body: 'Söhne Mono, weight 400, size 13px, uppercase letter-spacing 0.15em',
    },
    layout: 'fullscreen video bg; centered tagline with one short sentence; bottom-left video credits + bottom-right scroll-down indicator',
    motion: 'video autoplays muted+loop; headline letters fade-up on load (stagger 80ms); custom scroll-down arrow with vertical bounce; cursor reveals a "play reel" prompt over video area',
    libraries: ['hls.js or @mux/mux-player-react', 'framer-motion'],
    inspiration: ['apple.com hero', 'rivian.com', 'a24films.com'],
  },
};

export const listStyles = () => Object.keys(styles);
