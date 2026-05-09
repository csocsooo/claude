export default function Footer() {
  return (
    <footer className="border-t border-white/5 bg-ink-950 px-6 py-16">
      <div className="mx-auto grid max-w-7xl gap-10 md:grid-cols-4">
        <div className="md:col-span-1">
          <div className="mb-4 flex items-center gap-3">
            <img src="/logo.svg" alt="" className="h-8 w-auto" />
            <span className="font-display text-lg font-bold">__BRAND_NAME__</span>
          </div>
          <p className="max-w-xs text-sm text-neutral-500">__FOOTER_TAGLINE__</p>
        </div>

        <FooterCol
          title="__FOOTER_COL1_TITLE__"
          links={[
            { href: '#services', label: '__FOOTER_LINK_1__' },
            { href: '#projects', label: '__FOOTER_LINK_2__' },
            { href: '#contact', label: '__FOOTER_LINK_3__' },
          ]}
        />

        <FooterCol
          title="__FOOTER_COL2_TITLE__"
          links={[
            { href: '/impresszum', label: '__FOOTER_LEGAL_1__' },
            { href: '/adatkezeles', label: '__FOOTER_LEGAL_2__' },
            { href: '/aszf', label: '__FOOTER_LEGAL_3__' },
          ]}
        />

        <div>
          <h3 className="mb-4 text-sm font-semibold uppercase tracking-wider text-neutral-300">
            __FOOTER_COL3_TITLE__
          </h3>
          <ul className="space-y-2 text-sm text-neutral-500">
            <li>__FOOTER_ADDRESS__</li>
            <li>
              <a href="mailto:__FOOTER_EMAIL__" className="hover:text-white">
                __FOOTER_EMAIL__
              </a>
            </li>
            <li>
              <a href="tel:__FOOTER_PHONE__" className="hover:text-white">
                __FOOTER_PHONE__
              </a>
            </li>
          </ul>
        </div>
      </div>

      <div className="mx-auto mt-12 max-w-7xl border-t border-white/5 pt-6 text-center text-xs text-neutral-600">
        © __FOOTER_YEAR__ __BRAND_NAME__. __FOOTER_RIGHTS__
      </div>
    </footer>
  )
}

function FooterCol({
  title,
  links,
}: {
  title: string
  links: { href: string; label: string }[]
}) {
  return (
    <div>
      <h3 className="mb-4 text-sm font-semibold uppercase tracking-wider text-neutral-300">
        {title}
      </h3>
      <ul className="space-y-2 text-sm text-neutral-500">
        {links.map((l) => (
          <li key={l.href}>
            <a href={l.href} className="hover:text-white">
              {l.label}
            </a>
          </li>
        ))}
      </ul>
    </div>
  )
}
