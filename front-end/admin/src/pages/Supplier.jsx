import SupplierTable from '../components/supplier/SupplierTable';
import Page from '../components/reusable/Page';

function Supplier() {
    const heading = 'Suppliers';
    const text = 'Manage companies and individuals used to acquire materials for work orders.';

    return (
        <Page heading={heading} text={text}>
            <SupplierTable />
        </Page>
    )
}

export default Supplier;
