# MotionSites Generator

Magyar útmutató + Node.js CLI, ami a [motionsites.ai](https://motionsites.ai)
fizetős prompt-könyvtárának visszafejtett **mintái** alapján gyárt
"hero section" promptokat — amiket átmásolhatsz Lovable / Bolt.new / v0 /
Claude / Cursor felé, és kiad egy látványos, animált landing page hero-t.

> Nem a MotionSites prompttartalmát másolja (azokhoz nem fértem hozzá),
> hanem a **szerkezetet** és a **minta-felépítést** rekonstruálja a
> nyilvánosan elérhető címkékből, kategóriákból és JS bundle-ből.

---

## Mit tanultam a MotionSites-ról

| Mit csinálnak | Hogyan |
|---|---|
| Termék | Fizetős hero section prompt-könyvtár (~60+ prompt) |
| Bevétel | Havi / éves / lifetime előfizetés (Tolt affiliate, Stripe) |
| Tech | React SPA + Supabase backend + Mux videó-previewek |
| Felhasználás | Másold a promptot Lovable / Bolt / Google AI Studio-ba → kapsz egy kész animált hero-t |

**Felfedezett kategóriák:** SaaS, Portfolio (Dark / Bold / Cosmic), Agency
(Glassmorphism), AI / AI Automation, Web3, Crypto Wealth, Email Marketing,
Video, Automotive, Logistics, Space Voyage, Digital Reality.

**Felfedezett prompt-slugok (kivonat):** `aethera-hero`, `bionova-hero`,
`bloom-ai-hero`, `crypto-wealth-hero`, `datacore-booking-hero`,
`duolingo-styleguide-hero`, `glassmorphism-agency-hero`, `neuralyn-hero`,
`orbit-web3-hero`, `velorah-hero`, `vortex-studio-hero`,
`wealth-video-hero` … (összesen 60+).

---

## A MotionSites-mintázat (recept)

Minden jó hero-prompt **ugyanezt a 8 réteget** írja le explicit módon:

1. **Brand & one-liner** — kit vagy, mit csinálsz
2. **Hangulat** — egy mondat: pl. *"premium, airy, soft-futuristic"*
3. **Színpaletta** — háttér, surface, szöveg, accent — pontos hex / leírás
4. **Tipográfia** — display + body fontstack, súly, méret-clamp, tracking
5. **Layout** — térbeli rendezés egy mondatban
6. **Motion & interakció** — mit mozog, mikor, milyen library-vel
7. **Copy** — headline-formula + alcím-pattern + 2 CTA + social proof
8. **Tech & accessibility** — framework, libs, responsive, prefers-reduced-motion

A `templates/styles.mjs` 7 előre megírt stílusrecept (esztétikai csomag),
a `templates/industries.mjs` 9 iparági pozicionálási sablont (copy-formulát)
tartalmaz. A `prompt-builder.mjs` ezeket kombinálja.

---

## Használat

```bash
# Listázza az iparágakat és stílusokat
node generator.mjs --list

# Generálj egy promptot
node generator.mjs \
  --industry saas \
  --style saasGradient \
  --name "Apex" \
  --tagline "the CRM teams actually use" \
  --audience "post-Series-A revops teams" \
  --framework react+tailwind

# A kimenetet másold be Lovable / Bolt.new / v0 / Claude / Cursor felé.
```

### Opcionális flagek

| Flag | Mire való | Default |
|---|---|---|
| `--industry` | iparág kulcs (`saas`, `portfolio`, `web3` …) | **kötelező** |
| `--style` | stílus kulcs (`glassmorphism`, `darkCosmic` …) | iparág első ajánlása |
| `--name` | brand neve | `Acme` |
| `--tagline` | egysoros pozícionálás | placeholder |
| `--audience` | célközönség | `modern teams` |
| `--framework` | `react+tailwind` / `next` / `html` / `vue` | `react+tailwind` |
| `--extras` | pontosvesszővel elválasztott extra megjegyzések | — |

---

## Példa hero oldalak (`examples/`)

3 készre csiszolt, önmagában futtatható HTML — a generátor által
kiadott prompt **eredménye** lehetne, csak már kézzel megírva, hogy lásd
hova céloz a stílus.

| Fájl | Stílus | Iparág | Mit demonstrál |
|---|---|---|---|
| `examples/glassmorphism-saas.html` | Glassmorphism | SaaS | gradient mesh + frosted glass kártyák + mouse-parallax + word-stagger reveal |
| `examples/dark-portfolio.html` | Dark Cosmic | Designer portfolio | egyedi kurzor + radiális glow follow + serif italic display + függőleges marquee |
| `examples/web3-3d.html` | Web3 Neon 3D | Crypto / Web3 | Three.js iridescent torus knot custom shaderrel + animated grid floor + count-up stats |

Megnyitásuk: dupla klikk a HTML fájlra (semmilyen build / npm install nem kell).

---

## Hogyan adj hozzá új stílust vagy iparágat

**Új vizuális stílus:** `templates/styles.mjs` → adj hozzá egy új kulcsot
a `styles` objektumhoz, kövesd a meglévő struktúrát (mood, palette,
typography, layout, motion, libraries, inspiration).

**Új iparág:** `templates/industries.mjs` → új kulcs `headlineFormulas`,
`subheadlinePattern`, `ctas`, `socialProof`, `recommendedStyles`
mezőkkel.

A `prompt-builder.mjs`-t **nem** kell módosítani — automatikusan felveszi
az új sablonokat.

---

## Mire jó ez (és mire nem)

✅ **Jó** AI builder-ekhez (Lovable, Bolt, v0, Claude, Cursor) szóló
strukturált prompt gyors prototipizálásához.

✅ **Jó** ha tanulni akarod *milyen* az a "premium hero" esztétika és
hogyan kell pontosan leírni egy AI-nak, hogy reprodukálja.

❌ **Nem** helyettesíti a tényleges MotionSites előfizetést — az ő
prompttartalmuk valószínűleg jobban kicsiszolt, és Mux videó-previewekkel
tesztelt, kifizetett designerek által készített.

❌ **Nem** vágódesign rendszer — egy hero-szekciót generál, nem teljes
oldalt.
