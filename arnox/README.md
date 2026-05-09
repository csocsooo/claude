# Arnox — End-to-End validáció

Ez a mappa **a validációs lépés** a `motion-sites-generator` projekthez:

1. `prompt.md` — a `node generator.mjs --industry web3 --style web3Neon --name "Arnox" …` parancs kimenete
2. `index.html` — egy abszolút 3D motion landing page, amit ez a prompt **inspirált** (nem AI builder-rel generálva, hanem kézzel megépítve, hogy referencia legyen)

## Miért volt szükség erre

A 3 példa hero (`examples/`) önmagában csak hero-szekció volt. Az Arnox az első
**teljes többszekciós motion site**, ami megmutatja, mit jelent a recept
a "csak hero" szinten túl.

## Mit demonstrál

| Feature | Hol |
|---|---|
| Pinned full-viewport Three.js canvas | `#scene` — végig ott van a háttérben minden szekció alatt |
| Custom GLSL shader | iridescent fresnel + 3D simplex noise displacement, szín-uniformokkal |
| UnrealBloom postprocessing | a neon glow-hoz |
| GSAP master scroll-timeline | a teljes oldal scroll-progressén keresztül kamera + mesh + szín-mix scrub-elve |
| Pinned scroll szekció | `.how-track` — 3 lépés ScrollTrigger-rel váltogatva |
| Scroll-driven kamera dolly + parallax | a `sceneState` interpolált értékei a render loop-ban |
| Mouse parallax | finom kamera-offset egér mozgásra |
| Particle field | 1800 darab additive-blended pont egy gömbhéjon, lassan forog |
| Animált grid floor | CSS gradient + perspective transform |
| Glassmorphism feature kártyák | `backdrop-filter` + radial mouse-glow |
| Count-up számok | IntersectionObserver triggerelve |
| Hero text staggered reveal | GSAP timeline, `clip-path`-szerű overflow-hidden a szavakra |
| Reduced-motion fallback | minden animáció kikapcsol, statikus első frame |
| Reszponzív | `@media (max-width: 880px)` egyszerű, single-column mobile fallback |

## Megnyitás

```bash
# Bármi, ami statikusan kiszolgál (a Three.js modul-import miatt fontos a HTTP):
cd arnox && python3 -m http.server 8080
# majd: http://localhost:8080/
```

> **Megjegyzés:** dupla-klikkel (`file://`) az ES module import map működhet
> böngészőtől függően; ha a Three.js nem töltődne be, indítsd statikus
> szerveren (a fenti python3 parancs).

## Brand-koncepció

Arnox = "the compute fabric for autonomous agents." Egy kitalált web3 + AI
hibrid protokoll, ahol AI ügynökök bérelnek számítást, igazolják a végrehajtást
és fizetnek egymásnak — onchain, milliszekundumokban. A koncepció pont az a
fajta értékajánlat, ami megérdemli ezt a fajta vizuális kezelést (high-bloom,
shader-iridescence, aktív 3D), így validálja, hogy a recept tényleg ad
"premium" outputot.

## Felhasznált CDN-ek

- `three@0.160.0` (modul + addons via importmap)
- `gsap@3.12.5` + `ScrollTrigger`
- `Space Grotesk` + `IBM Plex Mono` (Google Fonts)

Egyetlen build step nincs, npm install nincs.
