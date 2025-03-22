import { Container } from 'react-bootstrap';

function Footer() {
    return (
        <footer className="footer bg-black small text-center text-white" aria-label="Footer">
            <Container className="px-4 px-lg-5">
                <span className="sr-only">Copyright</span> &copy; Oklahoma Handyman Service 2024
            </Container>
        </footer>
    );
}

export default Footer;
