function About() {
    return (
        <section className="about-section text-center" id="about" aria-label="About Oklahoma Handyman Service">
            <div className="container px-4 px-lg-5">
                <div className="row gx-4 gx-lg-5 justify-content-center">
                    <div className="col-lg-8">
                        <h2 className="text-white mb-4">Oklahoma Handyman Service</h2>
                        <p className="text-white">
                            We proudly offer a wide range of home repair and maintenance services throughout the central Oklahoma area.
                            Whether you need property maintenance, drywall repair, fence construction, or other home improvement tasks, we&apos;ve got you covered!
                        </p>
                    </div>
                </div>
                {/* <img className="img-fluid" src="assets/img/ipad.png" alt="Example of our handyman services in action" /> */}
            </div>
        </section>
    )
}

export default About;
