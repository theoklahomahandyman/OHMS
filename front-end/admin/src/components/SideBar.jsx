import PropTypes from 'prop-types';

function SideBar({ toggle, toggleSideBar }) {
    return (
        <ul className={toggle} id='accordionSidebar'>
            {/* <!-- Sidebar - Brand --> */}
            <a className="sidebar-brand d-flex align-items-center justify-content-center" href="/">
                <div className="sidebar-brand-icon rotate-n-15">
                    <i className="fas fa-tools"></i>
                </div>
                <div className="sidebar-brand-text mx-3"><b>OHMS</b></div>
            </a>
            {/* <!-- Divider --> */}
            <hr className="sidebar-divider my-0" />
            {/* <!-- Nav Item - Dashboard --> */}
            <li className="nav-item">
                <a className="nav-link" href="/">
                    <i className="fas fa-fw fa-tachometer-alt"></i>
                    <span>Dashboard</span>
                </a>
            </li>
            {/* <!-- Divider --> */}
            <hr className="sidebar-divider" />
            {/* <!-- Heading --> */}
            <div className="sidebar-heading">Users</div>
            {/* <!-- Nav Item - User Info Menu --> */}
            <li className="nav-item">
                <a className="nav-link collapsed" href="#" data-toggle="collapse" data-target="#userInfo" aria-expanded="true" aria-controls="userInfo">
                        <i className="fas fa-fw fa-user"></i>
                        <span>Profile</span>
                </a>
                <div id="userInfo" className="collapse" aria-labelledby="userInfo" data-parent="#accordionSidebar">
                    <div className="bg-white py-2 collapse-inner rounded">
                        <h6 className="collapse-header">User Information:</h6>
                        <a className="collapse-item" href="/profile/">Profile</a>
                        <a className="collapse-item" href="/password/">Password</a>
                    </div>
                </div>
            </li>
            {/* <!-- Nav Item - Admin Dashboard --> */}
            <li className="nav-item">
                <a className="nav-link" href="/admin/">
                    <i className="fas fa-fw fa-users"></i>
                    <span>Admin Dashboard</span>
                </a>
            </li>
            {/* <!-- Nav Item - Customer Dashboard --> */}
            <li className="nav-item">
                <a className="nav-link" href="/customer/">
                    <i className="fas fa-fw fa-user-circle"></i>
                    <span>Customer Dashboard</span>
                </a>
            </li>
            {/* <!-- Divider --> */}
            <hr className="sidebar-divider" />
            {/* <!-- Heading --> */}
            <div className="sidebar-heading">Work Orders</div>
            {/* <!-- Nav Item - Order Dashboard --> */}
            <li className="nav-item">
                <a className="nav-link" href="/order/">
                    <i className="fas fa-fw fa-file-invoice"></i>
                    <span>Order Dashboard</span>
                </a>
            </li>
            {/* <!-- Divider --> */}
            <hr className="sidebar-divider" />
            {/* <!-- Heading --> */}
            <div className="sidebar-heading">Inventory</div>
            {/* <!-- Nav Item - Purchase Dashboard --> */}
            <li className="nav-item">
                <a className="nav-link" href="/purchase/">
                    <i className="fas fa-fw fa-shopping-cart"></i>
                    <span>Purchase Dashboard</span>
                </a>
            </li>
            {/* <!-- Nav Item - Inventory Menu --> */}
            <li className="nav-item">
                <a className="nav-link collapsed" href="#" data-toggle="collapse" data-target="#inventory" aria-expanded="true" aria-controls="inventory">
                    <i className="fas fa-fw fa-tags"></i>
                    <span>Inventory</span>
                </a>
                <div id="inventory" className="collapse" aria-labelledby="inventory" data-parent="#accordionSidebar">
                    <div className="bg-white py-2 collapse-inner rounded">
                        <h6 className="collapse-header">Manage Inventory:</h6>
                        <a className="collapse-item" href="/supplier/">Supplier Dashboard</a>
                        <a className="collapse-item" href="/material/">Material Dashboard</a>
                        <a className="collapse-item"href="/tool" >Tool Dashboard</a>
                    </div>
                </div>
            </li>
            <li className="nav-item">
                <a className="nav-link" href="/service/">
                    <i className="fas fa-fw fa-screwdriver"></i>
                    <span>Service Types</span>
                </a>
            </li>
            {/* <!-- Sidebar Toggler (Sidebar) --> */}
            <div className="text-center d-none d-md-inline">
                <button className="rounded-circle border-0" id="sidebarToggle" onClick={toggleSideBar}></button>
            </div>
        </ul>
    )
}

SideBar.propTypes = {
    toggle: PropTypes.string.isRequired,
    toggleSideBar: PropTypes.func.isRequired
}

export default SideBar;
