import { Navbar, Nav, Container } from 'react-bootstrap';

function NavBar() {
    return (
        <Navbar expand="lg" className="navbar-light fixed-top" id="mainNav" aria-label="Navigation Bar for Oklahoma Handyman Service">
            <Container>
                {/* Brand logo */}
                <Navbar.Brand href="#page-top" aria-label="Oklahoma Handyman Service Home">OHMS</Navbar.Brand>
                {/* Toggle button for mobile */}
                <Navbar.Toggle aria-controls="navbarResponsive" aria-label="Toggle navigation bar" />
                {/* Collapsisble menu */}
                <Navbar.Collapse id="navbarResponsive">
                    <Nav className="ms-auto">
                        <Nav.Link href="#about">About</Nav.Link>
                        <Nav.Link href="#projects">Projects</Nav.Link>
                        <Nav.Link href="#contact-info">Contact Us</Nav.Link>
                    </Nav>
                </Navbar.Collapse>
            </Container>
        </Navbar>
    );
}

export default NavBar;
