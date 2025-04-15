import { ACCESS_TOKEN, REFRESH_TOKEN } from '../constants';
import { useNavigate } from 'react-router';
import { toast } from 'react-toastify';
import PropTypes from 'prop-types';
import Cookies from 'js-cookie';

function Nav({ toggleSideBar, setShowProfileModal }) {
    const navigate = useNavigate();

    const logout = () => {
        Cookies.remove(ACCESS_TOKEN);
        Cookies.remove(REFRESH_TOKEN);
        toast.success('Goodbye!');
        navigate('/login/');
    }

    return (
        <nav className="navbar navbar-expand navbar-light bg-white topbar mb-4 static-top shadow">
            {/* <!-- Sidebar Toggle (Topbar) --> */}
            <button id="sidebarToggleTop" className="btn btn-link d-md-none rounded-circle mr-3" onClick={toggleSideBar}>
                <i className="fa fa-bars"></i>
            </button>
            {/* <!-- Topbar Navbar --> */}
            <ul className="navbar-nav ml-auto">
                <div className="topbar-divider d-none d-sm-block"></div>
                {/* <!-- Nav Item - User Information --> */}
                <li className="nav-item dropdown no-arrow">
                    <a className="nav-link dropdown-toggle" href="#" id="userDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                        <i className="fas fa-user-circle img-profile rounded-circle fa-2x"></i>
                    </a>
                    {/* <!-- Dropdown - User Information --> */}
                    <div className="dropdown-menu dropdown-menu-right shadow animated--grow-in" aria-labelledby="userDropdown">
                        <button className="dropdown-item" onClick={() => setShowProfileModal(true)}>
                            <i className="fas fa-user fa-sm fa-fw mr-2 text-gray-400"></i>
                            Profile
                        </button>
                        <a className="dropdown-item" href="/password/">
                            <i className="fas fa-cogs fa-sm fa-fw mr-2 text-gray-400"></i>
                            Password
                        </a>
                        <div className="dropdown-divider"></div>
                        <button className="dropdown-item" onClick={logout}>
                            <i className="fas fa-sign-out-alt fa-sm fa-fw mr-2 text-gray-400"></i>
                            Logout
                        </button>
                    </div>
                </li>
            </ul>
        </nav>
    )
}

Nav.propTypes = {
    toggleSideBar: PropTypes.func.isRequired,
    setShowProfileModal: PropTypes.func.isRequired
};

export default Nav;
