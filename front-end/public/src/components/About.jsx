import { Container, Row, Col } from 'react-bootstrap';

function About() {
    return (
        <section className="about-section text-center" id="about" aria-label="About Oklahoma Handyman Service">
            <Container className="px-4 px-lg-5">
                <Row className="gx-4 gx-lg-5 justify-content-center">
                    <Col lg={8}>
                        <h3 className="text-white mb-4">Oklahoma Handyman Service</h3>
                        <p className="text-white">
                            We proudly offer a wide range of home repair and maintenance services throughout the central Oklahoma area.
                            Whether you need property maintenance, drywall repair, fence construction, or other home improvement tasks, we&apos;ve got you covered!
                            Check out our <a href="#projects" aria-label="View our completed projects">completed projects</a> to see our work in action
                        </p>
                        <p className="text-white">
                            Serving Moore, Oklahoma City, Norman, and the surrounding areas, we are committed to delivering quality craftsmanshsip and exceptional customer service.
                            Ready to start your project?{" "}
                            <a href="#contact" aria-label="Contact us for a quote">Contact us today</a>!
                        </p>
                    </Col>
                </Row>
                {/* <img className="img-fluid" src="assets/img/ipad.png" alt="Example of our handyman services in action" /> */}
            </Container>
        </section>
    );
}

export default About;
