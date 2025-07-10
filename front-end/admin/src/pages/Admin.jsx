import AdminTable from '../components/admin/AdminTable';
import Page from '../components/reusable/Page';

function Admin() {
    const heading = 'Administrators';
    const text = 'Administrators are other users for the admin area of the website.';

    return (
        <Page heading={heading} text={text}>
            <AdminTable />
        </Page>
    );
}

export default Admin;
