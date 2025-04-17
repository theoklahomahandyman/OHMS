import { useDispatch, useSelector } from 'react-redux';
import { setProfile } from '../../store/profileSlice';
import PasswordModal from '../profile/PasswordModal';
import ProfileModal from '../profile/ProfileModal';
import { useState, useEffect } from 'react';
import { profileAPI } from '../../api';
import PropTypes from 'prop-types';
import SideBar from '../SideBar';
import Footer from '../Footer';
import Nav from '../Nav';

function Page({ heading, text, children }) {
    const dispatch = useDispatch();
    const profile = useSelector(state => state.profile);

    const [toggle, setToggle] = useState('navbar-nav bg-gradient-primary sidebar sidebar-dark accordion');
    const [showProfileModal, setShowProfileModal] = useState(false);
    const [showPasswordModal, setShowPasswordModal] = useState(false);

    useEffect(() => {
        const fetchProfile = async () => {
            try {
                const response = await profileAPI.getProfile();
                dispatch(setProfile(response));
            } catch (error) {
                console.error('Profile load error:', error);
            }
        };
        if (!profile) fetchProfile();
    }, [dispatch, profile])

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
                <SideBar toggle={toggle} toggleSideBar={toggleSideBar} setShowProfileModal={setShowProfileModal} setShowPasswordModal={setShowPasswordModal} />
                <div id='content-wrapper' className='d-flex flex-column'>
                    <div id='content'>
                        <Nav toggleSideBar={toggleSideBar} setShowProfileModal={setShowProfileModal} setShowPasswordModal={setShowPasswordModal} />
                        <div className="container-fluid">
                            {heading ? <h1 className="h3 mb-2 text-gray-800 text-center">{heading}</h1> : <></>}
                            {text ? <p className="mb-4 text-center">{text}</p> : <></>}
                            {children}
                            <ProfileModal show={showProfileModal} onHide={() => setShowProfileModal(false)} />
                            <PasswordModal show={showPasswordModal} onHide={() => setShowPasswordModal(false)} />
                        </div>
                    </div>
                    <Footer />
                </div>
            </div>
            <a className="scroll-to-top rounded" href="#page-top">
                <i className="fas fa-angle-up"></i>
            </a>
        </>
    );
};

Page.propTypes = {
    heading: PropTypes.string,
    text: PropTypes.string,
    children: PropTypes.any
};

export default Page;
