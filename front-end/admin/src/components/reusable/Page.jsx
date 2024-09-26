import PropTypes from 'prop-types';
import { useState } from 'react';
import SideBar from '../SideBar';
import Footer from '../Footer';
import Nav from '../Nav';

function Page({ heading, text, children }) {
    const [toggle, setToggle] = useState('navbar-nav bg-gradient-primary sidebar sidebar-dark accordion');

    const toggleSideBar = () => {
        if (toggle === 'navbar-nav bg-gradient-primary sidebar sidebar-dark accordion') {
            setToggle('navbar-nav bg-gradient-primary sidebar sidebar-dark accordion toggled');
        } else {
            setToggle('navbar-nav bg-gradient-primary sidebar sidebar-dark accordion');
        }
    }

    return (
        <>
            <div id='wrapper'>
                <SideBar toggle={toggle} toggleSideBar={toggleSideBar} />
                <div id='content-wrapper' className='d-flex flex-column'>
                    <div id='content'>
                        <Nav toggleSideBar={toggleSideBar} />
                        <div className="container-fluid">
                            {heading ? <h1 className="h3 mb-2 text-gray-800 text-center">{heading}</h1> : <></>}
                            {text ? <p className="mb-4 text-center">{text}</p> : <></>}
                            {children}
                        </div>
                    </div>
                    <Footer />
                </div>
            </div>
            <a className="scroll-to-top rounded" href="#page-top">
                <i className="fas fa-angle-up"></i>
            </a>
        </>
    )
}

Page.propTypes = {
    heading: PropTypes.string,
    text: PropTypes.string,
    children: PropTypes.any
}

export default Page;
