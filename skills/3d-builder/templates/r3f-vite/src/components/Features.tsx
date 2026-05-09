import { useEffect, useRef } from 'react'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'

gsap.registerPlugin(ScrollTrigger)

const FEATURES = [
  { title: '__FEATURE_1_TITLE__', body: '__FEATURE_1_BODY__' },
  { title: '__FEATURE_2_TITLE__', body: '__FEATURE_2_BODY__' },
  { title: '__FEATURE_3_TITLE__', body: '__FEATURE_3_BODY__' },
]

export default function Features() {
  const sectionRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const ctx = gsap.context(() => {
      gsap.utils.toArray<HTMLElement>('.feature-card').forEach((el) => {
        gsap.from(el, {
          opacity: 0,
          y: 60,
          duration: 0.8,
          ease: 'power2.out',
          scrollTrigger: {
            trigger: el,
            start: 'top 80%',
          },
        })
      })
    }, sectionRef)
    return () => ctx.revert()
  }, [])

  return (
    <section
      ref={sectionRef}
      className="mx-auto max-w-6xl px-6 py-32 md:py-48"
    >
      <h2 className="mb-16 text-center text-4xl font-bold md:text-5xl">
        __FEATURES_HEADING__
      </h2>
      <div className="grid gap-8 md:grid-cols-3">
        {FEATURES.map((f, i) => (
          <div
            key={i}
            className="feature-card rounded-2xl border border-neutral-800 bg-neutral-900/50 p-8 backdrop-blur"
          >
            <h3 className="mb-3 text-xl font-semibold">{f.title}</h3>
            <p className="text-neutral-400">{f.body}</p>
          </div>
        ))}
      </div>
    </section>
  )
}
