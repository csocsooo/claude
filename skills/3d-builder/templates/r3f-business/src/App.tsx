import Nav from './components/Nav'
import Hero from './components/Hero'
import Services from './components/Services'
import ProjectShowcase from './components/ProjectShowcase'
import ContactForm from './components/ContactForm'
import Footer from './components/Footer'

export default function App() {
  return (
    <main className="relative">
      <Nav />
      <Hero />
      <Services />
      <ProjectShowcase />
      <ContactForm />
      <Footer />
    </main>
  )
}
