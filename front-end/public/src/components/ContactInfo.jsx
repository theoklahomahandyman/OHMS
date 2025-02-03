function ContactInfo() {
    return (
        <section className="contact-section bg-black" aria-label="Oklahoma Handyman Service Contact Information">
            <div className="container px-4 px-lg-5">
                <div className="row gx-4 gx-lg-5">
                    {/* Address */}
                    <div className="col-md-4 mb-3 mb-md-0">
                        <div className="card py-y h-100">
                            <div className="card-body text-center">
                                <i className="fas fa-map-marked-alt text-primary mb-2" aria-hidden="true"></i>
                                <h4 className="text-uppercase m-0">Location</h4>
                                <hr className="my-4 mx-auto" aria-hidden="true"/>
                                <div className="small text-black-50">
                                    <a href="https://www.google.com/maps/search/?api=1&query=Moore,Oklahoma" target="_blank" rel="noopener noreferrer" aria-label="Find us on Google Maps in Moore, Oklahoma">
                                        Moore, Oklahoma
                                    </a>
                                </div>
                            </div>
                        </div>
                    </div>
                    {/* Email */}
                    <div className="col-md-4 mb-3 mb-md-0">
                        <div className="card py-y h-100">
                            <div className="card-body text-center">
                                <i className="fas fa-envelope text-primary mb-2" aria-hidden="true"></i>
                                <h4 className="text-uppercase m-0">Email</h4>
                                <hr className="my-4 mx-auto" aria-hidden="true"/>
                                <div className="small text-black-50">
                                    <a href="mailto:cdkonstruction@gmail.com" aria-label="Email cdkonstruction@gmail.com">
                                        cdkonstruction@gmail.com
                                    </a>
                                </div>
                            </div>
                        </div>
                    </div>
                    {/* Phone */}
                    <div className="col-md-4 mb-3 mb-md-0">
                        <div className="card py-y h-100">
                            <div className="card-body text-center">
                                <i className="fas fa-mobile-alt text-primary mb-2" aria-hidden="true"></i>
                                <h4 className="text-uppercase m-0">Phone</h4>
                                <hr className="my-4 mx-auto" aria-hidden="true"/>
                                <div className="small text-black-50">
                                    <a href="tel:+19404526011" aria-label="Call +1 (940) 452-6011">+1 (940) 452-6011</a>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div className="social d-flex justify-content-center">
                    <a className="mx-2" href="https://www.facebook.com/profile.php?id=61554887921227" target="_blank" rel="noopener noreferrer" aria-label="Visit us on Facebook">
                        <i className="fab fa-facebook-f" aria-hidden="true"></i>
                        <span className="sr-only">Facebook</span>
                    </a>
                </div>
            </div>
        </section>
    )
}

export default ContactInfo;
