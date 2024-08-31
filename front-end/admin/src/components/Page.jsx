import SideBar from '../components/SideBar';
import Footer from '../components/Footer';
import Nav from '../components/Nav';
import PropTypes from 'prop-types';
import { useState } from 'react';

function Page({ children }) {
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
    children: PropTypes.any
}

export default Page;
