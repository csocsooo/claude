export default function Contact() {
  return (
    <section className="border-t border-neutral-800 bg-neutral-950 px-6 py-32">
      <div className="mx-auto max-w-3xl text-center">
        <h2 className="mb-6 text-4xl font-bold md:text-5xl">
          __CONTACT_HEADING__
        </h2>
        <p className="mb-10 text-neutral-400">__CONTACT_SUBTITLE__</p>
        <a
          href="mailto:hello@example.com"
          className="inline-block rounded-full bg-white px-8 py-4 font-semibold text-neutral-900 transition hover:scale-105"
        >
          __CONTACT_CTA__
        </a>
      </div>
    </section>
  )
}
