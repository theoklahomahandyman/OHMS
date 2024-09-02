import Table from '../components/reusable/Table';
import Page from '../components/reusable/Page';

function Customer() {

    const fields = [
        {name: 'first_name', label: 'First Name', type: 'text', required: true, maxLength: 100, minLength: 2},
        {name: 'last_name', label: 'Last Name', type: 'text', required: true, maxLength: 100, minLength: 2},
        {name: 'email', label: 'Email', type: 'email', required: true, maxLength: 255, minLength: 8},
        {name: 'phone', label: 'Phone Number', type: 'text', required: true, maxLength: 17, minLength: 16},
        {name: 'notes', label: 'Customer Notes', type: 'text', required: false, maxLength: 500}
    ];

    return (
        <Page>
            <h1 className="h3 mb-2 text-gray-800 text-center">Customers</h1>
            <p className="mb-4 text-center">
                Customers are the party that recieves the service provided in the work order and must be specified in an order.
            </p>
            <Table fields={fields} name='Customer' route='/customer/' />
        </Page>
    )
}

export default Customer;
