import Page from '../components/Page';

function Dashboard() {
    return (
        <Page>
            <h1 className="h3 mb-4 text-gray-800 text-center">Oklahoma Handyman Service Dashboard</h1>
            <div className="row">
                {/* <!-- Admin Dashboard Card --> */}
                <div className="col-lg-3 col-md-6 mb-4">
                    <div className="card shadow">
                        {/* <!-- Card Header - Accordion --> */}
                        <a href="#adminDashboardCard" className="d-block card-header py-3" data-toggle="collapse" role="button" aria-expanded="true" aria-controls="adminDashboardCard">
                            <h6 className="m-0 font-weight-bold text-primary text-center">Admin Dashboard</h6>
                        </a>
                        {/* <!-- Card Content - Collapse --> */}
                        <div className="collapse" id="adminDashboardCard">
                            <div className="card-body text-center">
                                <p className="text-center">The Admin Dashboard can be used to manage current site administrators.</p>
                                <a href="/admin/" className="btn btn-primary align-items-center" id="adminDashboardNavigation">Admin Dashboard</a>
                            </div>
                        </div>
                    </div>
                </div>
                {/* <!-- Profile Card --> */}
                <div className="col-lg-3 col-md-6 mb-4">
                    <div className="card shadow">
                        {/* <!-- Card Header - Accordion --> */}
                        <a href="#profileCard" className="d-block card-header py-3" data-toggle="collapse" role="button" aria-expanded="true" aria-controls="profileCard">
                            <h6 className="m-0 font-weight-bold text-primary text-center">Profile Dashboard</h6>
                        </a>
                        {/* <!-- Card Content - Collapse --> */}
                        <div className="collapse" id="profileCard">
                            <div className="card-body text-center">
                                <p className="text-center">
                                    The Profile Dashboard can be used to manage your current information.
                                    The Password Dashboard can be used to change your current password.
                                </p>
                                <a href="/profile/" className="btn btn-md btn-primary align-items-start" id="profileNavigation">Profile</a>
                                <a href="/password/" className="btn btn-md btn-primary align-items-end ml-2" id="passNavigation">Password</a>
                            </div>
                        </div>
                    </div>
                </div>
                {/* <!-- Customer Dashboard Card --> */}
                <div className="col-lg-3 col-md-6 mb-4">
                    <div className="card shadow">
                        {/* <!-- Card Header - Accordion --> */}
                        <a href="#customerDashboardCard" className="d-block card-header py-3" data-toggle="collapse" role="button" aria-expanded="true" aria-controls="customerDashboardCard">
                            <h6 className="m-0 font-weight-bold text-primary text-center">Customer Dashboard</h6>
                        </a>
                        {/* <!-- Card Content - Collapse --> */}
                        <div className="collapse" id="customerDashboardCard">
                            <div className="card-body text-center">
                                <p className="text-center">The Customer Dashboard can be used to manage past and current customers.</p>
                                <a href="/customer/" className="btn btn-primary align-items-center" id="customerDashboardNavigation">Customer Dashboard</a>
                            </div>
                        </div>
                    </div>
                </div>
                {/* <!-- Order Dashboard Card --> */}
                <div className="col-lg-3 col-md-6 mb-4">
                    <div className="card shadow">
                        {/* <!-- Card Header - Accordion --> */}
                        <a href="#orderDashboardCard" className="d-block card-header py-3" data-toggle="collapse" role="button" aria-expanded="true" aria-controls="orderDashboardCard">
                            <h6 className="m-0 font-weight-bold text-primary text-center">Order Dashboard</h6>
                        </a>
                        {/* <!-- Card Content - Collapse --> */}
                        <div className="collapse" id="orderDashboardCard">
                            <div className="card-body text-center">
                                <p className="text-center">The Order Dashboard can be used to manage past and current work orders.</p>
                                <a href="/order/" className="btn btn-primary align-items-center" id="orderDashboardNavigation">Order Dashboard</a>
                            </div>
                        </div>
                    </div>
                </div>
                {/* <!-- Material Dashboard Card --> */}
                <div className="col-lg-3 col-md-6 mb-4">
                    <div className="card shadow">
                        {/* <!-- Card Header - Accordion --> */}
                        <a href="#materialDashboardCard" className="d-block card-header py-3" data-toggle="collapse" role="button" aria-expanded="true" aria-controls="materialDashboardCard">
                            <h6 className="m-0 font-weight-bold text-primary text-center">Material Dashboard</h6>
                        </a>
                        {/* <!-- Card Content - Collapse --> */}
                        <div className="collapse" id="materialDashboardCard">
                            <div className="card-body text-center">
                                <p className="text-center">The Material Dashboard can be used to manage past and current materials.</p>
                                <a href="/material/" className="btn btn-primary align-items-center" id="materialDashboardNavigation">Material Dashboard</a>
                            </div>
                        </div>
                    </div>
                </div>
                {/* <!-- Purchase Dashboard Card --> */}
                <div className="col-lg-3 col-md-6 mb-4">
                    <div className="card shadow">
                        {/* <!-- Card Header - Accordion --> */}
                        <a href="#purchaseDashboardCard" className="d-block card-header py-3" data-toggle="collapse" role="button" aria-expanded="true" aria-controls="purchaseDashboardCard">
                            <h6 className="m-0 font-weight-bold text-primary text-center">Purchase Dashboard</h6>
                        </a>
                        {/* <!-- Card Content - Collapse --> */}
                        <div className="collapse" id="purchaseDashboardCard">
                            <div className="card-body text-center">
                                <p className="text-center">The Purchase Dashboard can be used to manage past and current purchases.</p>
                                <a href="/purchase/" className="btn btn-primary align-items-center" id="purchaseDashboardNavigation">Purchase Dashboard</a>
                            </div>
                        </div>
                    </div>
                </div>
                {/* <!-- Supplier Dashboard Card --> */}
                <div className="col-lg-3 col-md-6 mb-4">
                    <div className="card shadow">
                        {/* <!-- Card Header - Accordion --> */}
                        <a href="#supplierDashboardCard" className="d-block card-header py-3" data-toggle="collapse" role="button" aria-expanded="true" aria-controls="supplierDashboardCard">
                            <h6 className="m-0 font-weight-bold text-primary text-center">Supplier Dashboard</h6>
                        </a>
                        {/* <!-- Card Content - Collapse --> */}
                        <div className="collapse" id="supplierDashboardCard">
                            <div className="card-body text-center">
                                <p className="text-center">The Supplier Dashboard can be used to manage past and current suppliers.</p>
                                <a href="/supplier/" className="btn btn-primary align-items-center" id="supplierDashboardNavigation">Supplier Dashboard</a>
                            </div>
                        </div>
                    </div>
                </div>
                {/* <!-- Service Dashboard Card --> */}
                <div className="col-lg-3 col-md-6 mb-4">
                    <div className="card shadow">
                        {/* <!-- Card Header - Accordion --> */}
                        <a href="#serviceTypesCard" className="d-block card-header py-3" data-toggle="collapse" role="button" aria-expanded="true" aria-controls="serviceTypesCard">
                            <h6 className="m-0 font-weight-bold text-primary text-center">Service Types</h6>
                        </a>
                        {/* <!-- Card Content - Collapse --> */}
                        <div className="collapse" id="serviceTypesCard">
                            <div className="card-body text-center">
                                <p className="text-center">The Service Dashboard can be used to manage current service types.</p>
                                <a href="/service/" className="btn btn-primary align-items-center" id="serviceTypesNavigation">Service Dashboard</a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </Page>
    )
}

export default Dashboard;
