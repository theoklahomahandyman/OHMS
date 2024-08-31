function ContactForm() {
    return (
        <div>
            <section className="signup-section" id="contact">
                <div className="container px-4 px-lg-5">
                    <div className="row gx-4 gx-lg-5">
                        <div className="col-md-10 col-lg-8 mx-auto text-center">
                            <i className="far fa-paper-plane fa-2x mb-2 text-white"></i>
                            <h2 className="text-white mb-5">Contact us to get started with your project!</h2>
                            <form className="form" id="contactForm">
                                <div className="row mb-3">
                                    {/* <!-- First name input --> */}
                                    <div className="form-group col-md-6">
                                        <input type="text" id="firstName" name="firstName" className="form-control" required placeholder="John" minLength="2" maxLength="100" />
                                    </div>
                                    {/* <!-- Last name input --> */}
                                    <div className="form-group col-md-6">
                                        <input type="text" id="lastName" name="lastName" className="form-control" required placeholder="Doe" minLength="2" maxLength="100" />
                                    </div>
                                </div>
                                <div className="row mb-3">
                                    {/* <!-- Email input --> */}
                                    <div className="form-group col-md-6">
                                        <input type="email" id="email" name="email" className="form-control" required placeholder="johndoe@example.com" minLength="8" maxLength="255" />
                                    </div>
                                    {/* <!-- Confirm email input --> */}
                                    <div className="form-group col-md-6">
                                        <input type="email" id="confirmEmail" name="confirmEmail" className="form-control" required placeholder="johndoe@example.com" minLength="8" maxLength="255" />
                                    </div>
                                </div>
                                <div className="row mb-3">
                                    {/* <!-- Phone number input --> */}
                                    <div className="form-group col-md-6">
                                        <input type="text" id="phone" name="phone" className="form-control" required placeholder="1 (234) 567-8901" minLength="16" maxLength="17" />
                                    </div>
                                    {/* <!-- Optional pictures input --> */}
                                    <div className="form-group col-md-6">
                                        <input type="file" id="files" name="files" className="form-control" multiple />
                                    </div>
                                </div>
                                <div className="row mb-3">
                                    {/* <!-- Description input --> */}
                                    <div className="form-group col-12">
                                        <textarea id="description" name="description" className="form-control" required placeholder="Please write a description of the project..." minLength="150" maxLength="2000"></textarea>
                                    </div>
                                </div>
                                <div className="row mb-3">
                                    {/* <!-- Submit button --> */}
                                    <button id="submit" className="btn btn-primary" type="submit">Submit</button>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
            </section>
        </div>
    )
}

export default ContactForm;
