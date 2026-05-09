import { useEffect, useRef } from 'react'
import gsap from 'gsap'
import Scene from './Scene'

export default function Hero() {
  const titleRef = useRef<HTMLHeadingElement>(null)
  const subRef = useRef<HTMLParagraphElement>(null)
  const ctaRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const ctx = gsap.context(() => {
      gsap
        .timeline({ defaults: { ease: 'power3.out' } })
        .from(titleRef.current, { opacity: 0, y: 50, duration: 1.1 })
        .from(subRef.current, { opacity: 0, y: 25, duration: 0.9 }, '-=0.6')
        .from(ctaRef.current, { opacity: 0, y: 15, duration: 0.7 }, '-=0.5')
    })
    return () => ctx.revert()
  }, [])

  return (
    <section className="relative h-screen w-full overflow-hidden">
      <div className="absolute inset-0 z-0">
        <Scene />
      </div>

      <div className="absolute inset-0 z-[1] bg-gradient-to-b from-ink-950/40 via-transparent to-ink-950" />

      <div className="pointer-events-none relative z-10 flex h-full flex-col items-center justify-center px-6 text-center">
        <p className="mb-4 text-xs font-semibold uppercase tracking-[0.3em] text-brand-400">
          __HERO_KICKER__
        </p>
        <h1
          ref={titleRef}
          className="font-display text-5xl font-bold tracking-tight md:text-7xl lg:text-8xl"
        >
          __HERO_TITLE__
        </h1>
        <p
          ref={subRef}
          className="mt-6 max-w-2xl text-lg text-neutral-300 md:text-xl"
        >
          __HERO_SUBTITLE__
        </p>
        <div
          ref={ctaRef}
          className="pointer-events-auto mt-10 flex flex-wrap items-center justify-center gap-4"
        >
          <a
            href="#contact"
            className="rounded-full bg-brand-500 px-8 py-4 font-semibold text-ink-950 transition hover:scale-105 hover:bg-brand-400"
          >
            __HERO_CTA_PRIMARY__
          </a>
          <a
            href="#services"
            className="rounded-full border border-white/20 px-8 py-4 font-semibold text-white transition hover:bg-white/10"
          >
            __HERO_CTA_SECONDARY__
          </a>
        </div>
      </div>
    </section>
  )
}
