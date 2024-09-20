import Table from '../components/reusable/Table';
import Page from '../components/reusable/Page';

function Admin() {

    const fields = [
        {name: 'first_name', label: 'First Name', type: 'text', required: true, elementType: 'input', maxLength: 100, minLength: 2},
        {name: 'last_name', label: 'Last Name', type: 'text', required: true, elementType: 'input', maxLength: 100, minLength: 2},
        {name: 'email', label: 'Email', type: 'email', required: true, elementType: 'input', maxLength: 255, minLength: 8},
        {name: 'phone', label: 'Phone Number', type: 'text', required: true, elementType: 'input', maxLength: 17, minLength: 16},
        {name: 'is_active', label: 'Active', type: 'checkbox', required: false, elementType: 'input'},
    ];

    return (
        <Page>
            <h1 className="h3 mb-2 text-gray-800 text-center">Administrators</h1>
            <p className="mb-4 text-center">
                Administrators are other users for the admin area of the website.
            </p>
            <Table fields={fields} name='Administrator' route='/user/admin/' />
        </Page>
    )
}

export default Admin;
