function Projects() {
    return (
        <section className="projects-section bg-light" id="projects" aria-label="Oklahoma Handyman Service past projects">
            <div className="container px-4 px-lg-5">
                {/* Featured project row */}
                <article className="row gx-0 mb-4 mb-lg-5 align-items-center">
                    <div className="col-xl-8 col-lg-7">
                        <img src="/assets/img/construction-site.jpg" alt="Local construction site" className="img-fluid mb-3 mb-lg-0" aria-describedby="construction-site-desc" />
                        <p id="construction-site-desc" className="sr-only">This image  shows a construction site with concrete forms set up with rebar support, ready for the concrete to be poured.</p>
                    </div>
                    <div className="col-xl-4 col-lg-5">
                        <div className="featured-text text-center text-lg-left">
                            <h4>Our Work Speaks for Itself</h4>
                            <p className="text-black-50 mb-0">
                                Below, you&apos;ll find examples of some of our completed projects.
                                From wood staining to sheetrock repair, these photos showcase the quality craftsmanship and attention to detail we bring to every job.
                                Look at our work, and imagine what we can do for your home.
                            </p>
                        </div>
                    </div>
                </article>
                {/* Project 1 row */}
                <article className="row gx-0 mb-5 mb-lg-0 justify-content-center">
                    <div className="col-lg-6">
                        <img src="/assets/img/pergola-stain.jpg" alt="Outdoor pergola with fresh stain applied, showcasing a rich cedar color" className="img-fluid" aria-describedby="pergola-stain-desc" />
                        <p id="pergola-stain-desc" className="sr-only">This image  shows an outdoor pergola after being cleaned and restained.</p>
                    </div>
                    <div className="col-lg-6">
                        <div className="bg-black text-center h-100 project">
                            <div className="d-flex h-100">
                                <div className="project-text w-100 my-auto text-center text-lg-left">
                                    <h4 className="text-white">Wood Staining</h4>
                                    <p className="mb-0 text-white-50">
                                        This customer noticed the stain on his raw cedar pergola fading.
                                        After a couple of afternoons and a few coats of stain, we made the cedar look as if it was fresh from the mill.
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>
                </article>
                {/* Project 2 row */}
                <article className="row gx-0 justify-content-center">
                    <div className="col-lg-6">
                        <img src="/assets/img/drywall-repair.jpg" alt="Fixed drywall in a shower where paint and sheetrock were previously damaged" className="img-fluid" aria-describedby="drywall-repair-desc" />
                        <p id="drywall-repair-desc" className="sr-only">This image  shows a shower after the drywall repair was completed, with smooth, fresh paint applied.</p>
                    </div>
                    <div className="col-lg-6 order-lg-first">
                        <div className="bg-black text-center h-100 project">
                            <div className="d-flex h-100">
                                <div className="project-text w-100 my-auto text-center text-lg-right">
                                    <h4 className="text-white">Sheetrock Repair</h4>
                                    <p className="mb-0 text-white-50">
                                        This customer reached out because paint and sheetrock began falling on them in the shower.
                                        After a single afternoon, we were able to get it looking brand new again!
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>
                </article>
            </div>
        </section>
    )
}

export default Projects;
