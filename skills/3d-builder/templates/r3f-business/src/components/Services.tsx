import { useEffect, useRef } from 'react'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'
import {
  Compass,
  Hammer,
  Home,
  Key,
  Layers,
  Wallet,
  type LucideIcon,
} from 'lucide-react'

gsap.registerPlugin(ScrollTrigger)

interface Service {
  Icon: LucideIcon
  title: string
  body: string
}

// Claude: replace icons + copy with the user's actual services.
// Lucide gallery: https://lucide.dev/icons
const SERVICES: Service[] = [
  { Icon: Compass, title: '__SERVICE_1_TITLE__', body: '__SERVICE_1_BODY__' },
  { Icon: Hammer,  title: '__SERVICE_2_TITLE__', body: '__SERVICE_2_BODY__' },
  { Icon: Home,    title: '__SERVICE_3_TITLE__', body: '__SERVICE_3_BODY__' },
  { Icon: Key,     title: '__SERVICE_4_TITLE__', body: '__SERVICE_4_BODY__' },
  { Icon: Layers,  title: '__SERVICE_5_TITLE__', body: '__SERVICE_5_BODY__' },
  { Icon: Wallet,  title: '__SERVICE_6_TITLE__', body: '__SERVICE_6_BODY__' },
]

export default function Services() {
  const ref = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const ctx = gsap.context(() => {
      gsap.utils.toArray<HTMLElement>('.service-card').forEach((el, i) => {
        gsap.from(el, {
          opacity: 0,
          y: 60,
          duration: 0.7,
          delay: (i % 3) * 0.1,
          ease: 'power2.out',
          scrollTrigger: { trigger: el, start: 'top 85%' },
        })
      })
    }, ref)
    return () => ctx.revert()
  }, [])

  return (
    <section id="services" ref={ref} className="mx-auto max-w-7xl px-6 py-32">
      <div className="mx-auto mb-16 max-w-2xl text-center">
        <p className="mb-3 text-xs font-semibold uppercase tracking-[0.3em] text-brand-400">
          __SERVICES_KICKER__
        </p>
        <h2 className="font-display text-4xl font-bold md:text-5xl">
          __SERVICES_HEADING__
        </h2>
        <p className="mt-5 text-neutral-400">__SERVICES_SUBTITLE__</p>
      </div>

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {SERVICES.map(({ Icon, title, body }, i) => (
          <article
            key={i}
            className="service-card group rounded-2xl border border-white/5 bg-ink-900/40 p-8 backdrop-blur-sm transition hover:-translate-y-1 hover:border-brand-500/40 hover:bg-ink-900/70"
          >
            <div className="mb-6 inline-flex h-14 w-14 items-center justify-center rounded-xl bg-brand-500/10 text-brand-400 transition group-hover:scale-110 group-hover:bg-brand-500/20">
              <Icon size={28} strokeWidth={1.5} />
            </div>
            <h3 className="mb-3 text-xl font-semibold">{title}</h3>
            <p className="text-neutral-400">{body}</p>
          </article>
        ))}
      </div>
    </section>
  )
}
