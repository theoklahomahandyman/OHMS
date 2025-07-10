import { Container, Row, Col, ListGroup } from 'react-bootstrap';

function Sitemap() {
    return (
        <section className="bg-black text-white py-5" id="sitemap" aria-label="Oklahoma Handyman Service (OHMS) website navigation map">
            <Container>
                <Row className="justify-content-center">
                    <Col md={8} className="text-center">
                        <h2 className="mb-4">Site Navigation</h2>
                        <ListGroup horizontal className="justify-content-center flex-wrap">
                            <ListGroup.Item className="bg-transparent border-0">
                                <a href="#page-top" className="text-white text-decoration-none">Home</a>
                            </ListGroup.Item>
                            <ListGroup.Item className="bg-transparent border-0">
                                <a href="#about" className="text-white text-decoration-none">About</a>
                            </ListGroup.Item>
                            <ListGroup.Item className="bg-transparent border-0">
                                <a href="#projects" className="text-white text-decoration-none">Projects</a>
                            </ListGroup.Item>
                            <ListGroup.Item className="bg-transparent border-0">
                                <a href="#contact-info" className="text-white text-decoration-none">Contact</a>
                            </ListGroup.Item>
                            <ListGroup.Item className="bg-transparent border-0">
                                <a href="#sitemap" className="text-white text-decoration-none">Site Map</a>
                            </ListGroup.Item>
                        </ListGroup>
                    </Col>
                </Row>
            </Container>
        </section>
    );
}

export default Sitemap;
