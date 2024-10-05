import Table from '../components/reusable/Table';
import Page from '../components/reusable/Page';

function Admin() {
    const heading = 'Administrators';

    const text = 'Administrators are other users for the admin area of the website.';

    const fields = [
        {name: 'first_name', label: 'First Name', type: 'text', required: true, elementType: 'input', maxLength: 100, minLength: 2},
        {name: 'last_name', label: 'Last Name', type: 'text', required: true, elementType: 'input', maxLength: 100, minLength: 2},
        {name: 'email', label: 'Email', type: 'email', required: true, elementType: 'input', maxLength: 255, minLength: 8},
        {name: 'phone', label: 'Phone Number', type: 'text', required: true, elementType: 'input', maxLength: 17, minLength: 16},
        {name: 'pay_rate', label: 'Pay Rate', type: 'number', required: true, elementType: 'input', minValue: 0.0},
        {name: 'is_active', label: 'Active', type: 'checkbox', required: false, elementType: 'input'},
    ];

    return (
        <Page heading={heading} text={text}>
            <Table fields={fields} name='Administrator' route='/user/admin/' />
        </Page>
    )
}

export default Admin;
