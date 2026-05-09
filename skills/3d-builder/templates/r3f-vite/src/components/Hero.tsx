import { useEffect, useRef } from 'react'
import gsap from 'gsap'
import Scene from './Scene'

export default function Hero() {
  const titleRef = useRef<HTMLHeadingElement>(null)
  const subRef = useRef<HTMLParagraphElement>(null)

  useEffect(() => {
    const ctx = gsap.context(() => {
      gsap.from(titleRef.current, {
        opacity: 0,
        y: 40,
        duration: 1,
        ease: 'power3.out',
      })
      gsap.from(subRef.current, {
        opacity: 0,
        y: 20,
        duration: 1,
        delay: 0.3,
        ease: 'power3.out',
      })
    })
    return () => ctx.revert()
  }, [])

  return (
    <section className="relative h-screen w-full overflow-hidden">
      <div className="absolute inset-0 z-0">
        <Scene />
      </div>
      <div className="pointer-events-none relative z-10 flex h-full flex-col items-center justify-center px-6 text-center">
        <h1
          ref={titleRef}
          className="text-5xl font-extrabold tracking-tight md:text-7xl"
        >
          __HERO_TITLE__
        </h1>
        <p
          ref={subRef}
          className="mt-6 max-w-xl text-lg text-neutral-300 md:text-xl"
        >
          __HERO_SUBTITLE__
        </p>
      </div>
    </section>
  )
}
