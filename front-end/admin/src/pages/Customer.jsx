import Table from '../components/reusable/Table';
import Page from '../components/reusable/Page';

function Customer() {
    const heading = 'Customers';

    const text = 'Customers are the party that recieves the service provided in the work order and must be specified in an order.';

    const fields = [
        {name: 'first_name', label: 'First Name', type: 'text', required: true, elementType: 'input', maxLength: 100, minLength: 2},
        {name: 'last_name', label: 'Last Name', type: 'text', required: true, elementType: 'input', maxLength: 100, minLength: 2},
        {name: 'email', label: 'Email', type: 'email', required: true, elementType: 'input', maxLength: 255, minLength: 8},
        {name: 'phone', label: 'Phone Number', type: 'text', required: true, elementType: 'input', maxLength: 17, minLength: 16},
        {name: 'notes', label: 'Customer Notes', type: 'text', required: false, elementType: 'input', maxLength: 500}
    ];

    return (
        <Page heading={heading} text={text}>
            <Table fields={fields} name='Customer' route='/customer/' />
        </Page>
    )
}

export default Customer;
