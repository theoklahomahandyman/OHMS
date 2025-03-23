import { Container, Button } from 'react-bootstrap';

function Header() {
    return (
        <header className="masthead" id="page-top" aria-label="Main Header for Oklahoma Handyman Service">
            <Container className="px-4 px-lg-5 d-flex h-100 align-items-center justify-content-center">
                <div className="d-flex justify-content-center">
                    <div className="text-center">
                        <h1 className="mx-auto my-0 text-uppercase">Oklahoma Handyman Service</h1>
                        <h2 className="text-white-50 mx-auto mt-2 mb-5">Local Handyman Services</h2>
                        <Button variant="primary" href="#about" aria-label="Learn more about Oklahoma Handyman Service">About Us</Button>
                    </div>
                </div>
            </Container>
        </header>
    );
}

export default Header;
