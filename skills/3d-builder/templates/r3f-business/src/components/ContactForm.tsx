import { useState } from 'react'

type Status = 'idle' | 'sending' | 'success' | 'error'

export default function ContactForm() {
  const [status, setStatus] = useState<Status>('idle')
  const endpoint = import.meta.env.VITE_FORMSPREE_ENDPOINT as string | undefined

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault()
    if (!endpoint) {
      console.warn('VITE_FORMSPREE_ENDPOINT not set — see .env.example')
      setStatus('error')
      return
    }
    setStatus('sending')
    const form = e.currentTarget
    const data = new FormData(form)
    try {
      const res = await fetch(endpoint, {
        method: 'POST',
        body: data,
        headers: { Accept: 'application/json' },
      })
      if (res.ok) {
        setStatus('success')
        form.reset()
      } else {
        setStatus('error')
      }
    } catch {
      setStatus('error')
    }
  }

  return (
    <section
      id="contact"
      className="relative border-t border-white/5 px-6 py-32"
    >
      <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_top,_rgba(255,255,255,0.04),_transparent_60%)]" />

      <div className="relative mx-auto max-w-2xl">
        <div className="mb-12 text-center">
          <p className="mb-3 text-xs font-semibold uppercase tracking-[0.3em] text-brand-400">
            __CONTACT_KICKER__
          </p>
          <h2 className="font-display text-4xl font-bold md:text-5xl">
            __CONTACT_HEADING__
          </h2>
          <p className="mt-4 text-neutral-400">__CONTACT_SUBTITLE__</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-5" noValidate>
          <div className="grid gap-5 md:grid-cols-2">
            <Field name="name" type="text" required label="__FORM_NAME_LABEL__" />
            <Field name="email" type="email" required label="__FORM_EMAIL_LABEL__" />
          </div>
          <Field name="phone" type="tel" label="__FORM_PHONE_LABEL__" />
          <Field
            name="message"
            type="textarea"
            required
            label="__FORM_MESSAGE_LABEL__"
          />

          <label className="flex items-start gap-3 text-sm text-neutral-400">
            <input
              required
              type="checkbox"
              name="gdpr"
              className="mt-1 h-4 w-4 accent-brand-500"
            />
            <span>__FORM_GDPR_LABEL__</span>
          </label>

          <button
            type="submit"
            disabled={status === 'sending'}
            className="w-full rounded-full bg-brand-500 px-8 py-4 font-semibold text-ink-950 transition hover:bg-brand-400 disabled:opacity-60"
          >
            {status === 'sending' ? '__FORM_SENDING__' : '__FORM_SUBMIT__'}
          </button>

          {status === 'success' && (
            <p role="status" className="text-center text-green-400">
              __FORM_SUCCESS__
            </p>
          )}
          {status === 'error' && (
            <p role="alert" className="text-center text-red-400">
              __FORM_ERROR__
            </p>
          )}
        </form>
      </div>
    </section>
  )
}

function Field({
  name,
  type,
  label,
  required = false,
}: {
  name: string
  type: 'text' | 'email' | 'tel' | 'textarea'
  label: string
  required?: boolean
}) {
  const className =
    'w-full rounded-lg border border-white/10 bg-ink-900/60 px-4 py-3 text-white placeholder-neutral-500 transition focus:border-brand-400 focus:outline-none focus:ring-2 focus:ring-brand-500/30'
  return (
    <label className="block">
      <span className="mb-2 block text-sm font-medium text-neutral-300">
        {label} {required && <span className="text-brand-400">*</span>}
      </span>
      {type === 'textarea' ? (
        <textarea name={name} required={required} rows={5} className={className} />
      ) : (
        <input name={name} type={type} required={required} className={className} />
      )}
    </label>
  )
}
