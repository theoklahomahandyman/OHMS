import CustomerTable from '../components/customer/CustomerTable';
import Page from '../components/reusable/Page';

function Customer() {
    const heading = 'Customers';
    const text = 'Customers are the party that recieves the service provided in the work order and must be specified in an order.';

    return (
        <Page heading={heading} text={text}>
            <CustomerTable />
        </Page>
    );
};

export default Customer;
