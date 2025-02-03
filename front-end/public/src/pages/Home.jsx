import ContactForm from '../components/ContactForm';
import ContactInfo from '../components/ContactInfo';
import Projects from '../components/Projects';
import Footer from '../components/Footer';
import Header from '../components/Header';
import About from '../components/About';
import Nav from '../components/Nav';

function Home() {
    return (
        <>
            <Nav />
            <Header />
            <About />
            <Projects />
            <ContactForm />
            <ContactInfo />
            <Footer />
        </>
    )
}

export default Home;
