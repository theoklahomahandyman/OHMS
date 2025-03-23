import { Container, Row, Col, Card } from 'react-bootstrap';

function ContactInfo() {
    return (
        <section className="contact-section bg-black" aria-label="Oklahoma Handyman Service Contact Information">
            <Container className="px-4 px-lg-5">
                <Row className="gx-4 gx-lg-5">
                    {/* Address */}
                    <Col md={4} className="mb-3 mb-md-0">
                        <Card className="h-100 border-0">
                            <Card.Body className="text-center">
                                <i className="fas fa-map-marked-alt text-primary mb-2" aria-hidden="true"></i>
                                <Card.Title as="h4" className="text-uppercase m-0">Location</Card.Title>
                                <hr className="my-4 mx-auto" aria-hidden="true"/>
                                <Card.Text className="small text-black-50">
                                    <a href="https://www.google.com/maps/search/?api=1&query=Moore,Oklahoma" target="_blank" rel="noopener noreferrer" aria-label="Find us on Google Maps in Moore, Oklahoma">
                                        Moore, Oklahoma
                                    </a>
                                </Card.Text>
                            </Card.Body>
                        </Card>
                    </Col>
                    {/* Email */}
                    <Col md={4} className="mb-3 mb-md-0">
                        <Card className="h-100 border-0">
                            <Card.Body className="text-center">
                                <i className="fas fa-envelope text-primary mb-2" aria-hidden="true"></i>
                                <Card.Title as="h4" className="text-uppercase m-0">Email</Card.Title>
                                <hr className="my-4 mx-auto" aria-hidden="true"/>
                                <Card.Text className="small text-black-50">
                                    <a href="mailto:cdkonstruction@gmail.com" aria-label="Email cdkonstruction@gmail.com">
                                        cdkonstruction@gmail.com
                                    </a>
                                </Card.Text>
                            </Card.Body>
                        </Card>
                    </Col>
                    {/* Phone */}
                    <Col md={4} className="mb-3 mb-md-0">
                        <Card className="py-y h-100">
                            <Card.Body className="text-center">
                                <i className="fas fa-mobile-alt text-primary mb-2" aria-hidden="true"></i>
                                <Card.Title as="h4" className="text-uppercase m-0">Phone</Card.Title>
                                <hr className="my-4 mx-auto" aria-hidden="true"/>
                                <Card.Text className="small text-black-50">
                                    <a href="tel:+19404526011" aria-label="Call +1 (940) 452-6011">+1 (940) 452-6011</a>
                                </Card.Text>
                            </Card.Body>
                        </Card>
                    </Col>
                </Row>
                <div className="social d-flex justify-content-center">
                    <a className="mx-2" href="https://www.facebook.com/profile.php?id=61554887921227" target="_blank" rel="noopener noreferrer" aria-label="Visit us on Facebook">
                        <i className="fab fa-facebook-f" aria-hidden="true"></i>
                        <span className="sr-only">Facebook</span>
                    </a>
                </div>
            </Container>
        </section>
    )
}

export default ContactInfo;
