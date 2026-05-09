import { useEffect, useRef, useState } from 'react'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'

gsap.registerPlugin(ScrollTrigger)

const IMAGES = [
  { src: '/projects/1.jpg', alt: '__PROJECT_IMG_1_ALT__' },
  { src: '/projects/2.jpg', alt: '__PROJECT_IMG_2_ALT__' },
  { src: '/projects/3.jpg', alt: '__PROJECT_IMG_3_ALT__' },
  { src: '/projects/4.jpg', alt: '__PROJECT_IMG_4_ALT__' },
]

const STATS = [
  { label: '__STAT_1_LABEL__', value: '__STAT_1_VALUE__' },
  { label: '__STAT_2_LABEL__', value: '__STAT_2_VALUE__' },
  { label: '__STAT_3_LABEL__', value: '__STAT_3_VALUE__' },
]

export default function ProjectShowcase() {
  const sectionRef = useRef<HTMLElement>(null)
  const [imgIndex, setImgIndex] = useState(0)

  useEffect(() => {
    const el = sectionRef.current
    if (!el) return
    const ctx = gsap.context(() => {
      ScrollTrigger.create({
        trigger: el,
        start: 'top top',
        end: 'bottom bottom',
        scrub: 1,
        onUpdate: (self) => {
          const idx = Math.min(
            IMAGES.length - 1,
            Math.floor(self.progress * IMAGES.length),
          )
          setImgIndex(idx)
        },
      })
    }, sectionRef)
    return () => ctx.revert()
  }, [])

  return (
    <section
      id="projects"
      ref={sectionRef}
      className="relative h-[400vh] bg-ink-950"
    >
      <div className="sticky top-0 flex h-screen w-full items-center overflow-hidden">
        <div className="mx-auto grid w-full max-w-7xl grid-cols-1 items-center gap-12 px-6 md:grid-cols-2">
          <div>
            <p className="mb-3 text-xs font-semibold uppercase tracking-[0.3em] text-brand-400">
              __PROJECT_KICKER__
            </p>
            <h2 className="mb-6 font-display text-4xl font-bold md:text-6xl">
              __PROJECT_TITLE__
            </h2>
            <p className="mb-10 text-lg text-neutral-300">__PROJECT_BODY__</p>

            <dl className="grid grid-cols-3 gap-6 border-t border-white/10 pt-8">
              {STATS.map((s, i) => (
                <div key={i}>
                  <dt className="text-xs uppercase tracking-wider text-neutral-500">
                    {s.label}
                  </dt>
                  <dd className="mt-1 font-display text-2xl font-bold text-brand-400">
                    {s.value}
                  </dd>
                </div>
              ))}
            </dl>
          </div>

          <div className="relative aspect-[4/3] overflow-hidden rounded-2xl border border-white/10 bg-ink-900 shadow-2xl">
            {IMAGES.map((img, i) => (
              <img
                key={i}
                src={img.src}
                alt={img.alt}
                loading="lazy"
                className={`absolute inset-0 h-full w-full object-cover transition-opacity duration-700 ${
                  i === imgIndex ? 'opacity-100' : 'opacity-0'
                }`}
              />
            ))}
            <div className="pointer-events-none absolute inset-0 bg-gradient-to-t from-ink-950/40 via-transparent to-transparent" />
            <div className="absolute bottom-4 left-4 right-4 flex justify-between text-xs text-white/80">
              <span>{IMAGES[imgIndex].alt}</span>
              <span>
                {imgIndex + 1} / {IMAGES.length}
              </span>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
