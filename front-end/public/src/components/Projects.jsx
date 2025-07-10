import { Container, Row, Col, Card } from 'react-bootstrap';

function Projects() {
    return (
        <section className="projects-section bg-light" id="projects" aria-label="Oklahoma Handyman Service past projects">
            <Container>
                {/* Featured project row */}
                <Row className="gx-0 mb-4 mb-lg-5 align-items-center">
                    <Col xl={8} lg={7}>
                        <img role="img" src="/assets/img/construction-site.jpg" alt="Local construction site" loading="lazy" decoding="async" className="img-fluid rounded mb-3 mb-lg-0" aria-describedby="construction-site-desc" />
                        <p id="construction-site-desc" className="sr-only">This image  shows a construction site with concrete forms set up with rebar support, ready for the concrete to be poured.</p>
                    </Col>
                    <Col xl={4} lg={5}>
                        <Card className="border-0 bg-light h-100">
                            <Card.Body className="text-center text-lg-left">
                                <Card.Title as="h3">Our Work Speaks for Itself</Card.Title>
                                <Card.Text className="text-black-50">
                                    Below, you&apos;ll find examples of some of our completed projects.
                                    From wood staining to sheetrock repair, these photos showcase the quality craftsmanship and attention to detail we bring to every job.
                                    Look at our work, and imagine what we can do for your home.
                                    Ready to start your project?{" "}
                                    <a href="#contact-info" aria-label="Contact us for a quote">Contact us today</a>!
                                </Card.Text>
                            </Card.Body>
                        </Card>
                    </Col>
                </Row>
                {/* Project 1 row */}
                <Row className="gx-0 mb-5 mb-lg-0 justify-content-center align-items-stretch">
                    <Col lg={6}>
                        <img role="img" src="/assets/img/pergola-stain.jpg" alt="Pergola staining service in Moore, Oklahoma by OHMS" loading="lazy" decoding="async" className="img-fluid rounded mb-3" aria-describedby="pergola-stain-desc" />
                        <p id="pergola-stain-desc" className="sr-only">This image  shows an outdoor pergola after being cleaned and restained.</p>
                    </Col>
                    <Col lg={6} className="mb-3">
                        <Card className="bg-black text-white h-100">
                            <Card.Body className="d-flex flex-column justify-content-center text-center text-lg-left">
                                <Card.Title as="h3" className="text-white">Wood Staining</Card.Title>
                                <Card.Text className="text-white-50">
                                    This customer noticed the stain on his raw cedar pergola fading.
                                    After a couple of afternoons and a few coats of stain, we made the cedar look as if it was fresh from the mill.
                                    Interested in wood staining for your home?{" "}
                                    <a href="#contact-info" aria-label="Contact us for wood staining services">Get a free quote</a>!
                                </Card.Text>
                            </Card.Body>
                        </Card>
                    </Col>
                </Row>
                {/* Project 2 row */}
                <Row className="gx-0 justify-content-center align-items-stretch">
                    <Col lg={6}>
                        <img role="img" src="/assets/img/drywall-repair.jpg" alt="Fixed drywall in a shower where paint and sheetrock were previously damaged" loading="lazy" decoding="async" className="img-fluid rounded mb-3" aria-describedby="drywall-repair-desc" />
                        <p id="drywall-repair-desc" className="sr-only">This image  shows a shower after the drywall repair was completed, with smooth, fresh paint applied.</p>
                    </Col>
                    <Col lg={6} className="order-lg-first mb-3">
                        <Card className="bg-black text-white h-100">
                            <Card.Body className="d-flex flex-column justify-content-center text-center text-lg-right">
                                <Card.Title as="h3" className="text-white">Sheetrock Repair</Card.Title>
                                <Card.Text className="text-white-50">
                                    This customer reached out because paint and sheetrock began falling on them in the shower.
                                    After a single afternoon, we were able to get it looking brand new again!
                                    Need drywall repair?{" "}
                                    <a href="#contact-info" aria-label="Schedule drywall repair appointment">Schedule an appointment</a>!
                                </Card.Text>
                            </Card.Body>
                        </Card>
                    </Col>
                </Row>
            </Container>
        </section>
    );
}

export default Projects;
