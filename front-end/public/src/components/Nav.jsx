function Nav() {
    return (
        <nav className="navbar navbar-expand-lg navbar-light fixed-top" id="mainNav" aria-label="Navigation Bar for Oklahoma Handyman Service">
            <div className="container px-4 px-lg-5 d-flex justify-content-between">
                <a className="navbar-brand" href="#page-top" aria-label="Oklahoma Handyman Service Home">OHMS</a>
                <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarResponsive"
                    aria-controls="navbarResponsive" aria-expanded="false" aria-label="Toggle navigation bar">
                    <span className="navbar-toggler-icon"></span>
                </button>
                <div className="collapse navbar-collapse" id="navbarResponsive">
                    <ul className="navbar-nav ms-auto">
                        <li className="nav-item"><a className="nav-link" href="#about">About</a></li>
                        <li className="nav-item"><a className="nav-link" href="#projects">Projects</a></li>
                        <li className="nav-item"><a className="nav-link" href="#contact">Contact</a></li>
                    </ul>
                </div>
            </div>
        </nav>
    )
}

export default Nav;
