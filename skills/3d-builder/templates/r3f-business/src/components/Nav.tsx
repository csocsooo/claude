import { useEffect, useState } from 'react'
import { Menu, X } from 'lucide-react'

const LINKS = [
  { href: '#services', label: '__NAV_SERVICES__' },
  { href: '#projects', label: '__NAV_PROJECTS__' },
  { href: '#contact', label: '__NAV_CONTACT__' },
]

export default function Nav() {
  const [scrolled, setScrolled] = useState(false)
  const [open, setOpen] = useState(false)

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 20)
    window.addEventListener('scroll', onScroll, { passive: true })
    return () => window.removeEventListener('scroll', onScroll)
  }, [])

  return (
    <nav
      className={`fixed inset-x-0 top-0 z-50 transition-colors ${
        scrolled ? 'bg-ink-950/85 backdrop-blur-md border-b border-white/5' : 'bg-transparent'
      }`}
    >
      <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
        <a href="#" className="flex items-center gap-3" aria-label="__BRAND_NAME__">
          <img src="/logo.svg" alt="" className="h-8 w-auto" />
          <span className="font-display text-xl font-bold tracking-tight">
            __BRAND_NAME__
          </span>
        </a>

        <ul className="hidden items-center gap-8 md:flex">
          {LINKS.map((l) => (
            <li key={l.href}>
              <a
                href={l.href}
                className="text-sm font-medium text-neutral-300 transition hover:text-white"
              >
                {l.label}
              </a>
            </li>
          ))}
        </ul>

        <a
          href="#contact"
          className="hidden rounded-full bg-brand-500 px-5 py-2 text-sm font-semibold text-ink-950 transition hover:bg-brand-400 md:inline-block"
        >
          __NAV_CTA__
        </a>

        <button
          type="button"
          onClick={() => setOpen((s) => !s)}
          className="md:hidden"
          aria-label="Toggle menu"
          aria-expanded={open}
        >
          {open ? <X size={24} /> : <Menu size={24} />}
        </button>
      </div>

      {open && (
        <div className="border-t border-white/5 bg-ink-950/95 backdrop-blur-md md:hidden">
          <ul className="flex flex-col gap-1 px-6 py-4">
            {LINKS.map((l) => (
              <li key={l.href}>
                <a
                  href={l.href}
                  onClick={() => setOpen(false)}
                  className="block rounded-lg px-3 py-3 text-base text-neutral-200 hover:bg-white/5"
                >
                  {l.label}
                </a>
              </li>
            ))}
            <li>
              <a
                href="#contact"
                onClick={() => setOpen(false)}
                className="mt-2 block rounded-full bg-brand-500 px-5 py-3 text-center font-semibold text-ink-950"
              >
                __NAV_CTA__
              </a>
            </li>
          </ul>
        </div>
      )}
    </nav>
  )
}
