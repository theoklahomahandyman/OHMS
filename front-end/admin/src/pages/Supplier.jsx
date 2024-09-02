import Table from '../components/reusable/Table';
import Page from '../components/reusable/Page';

function Supplier() {

    const fields = [
        {name: 'name', label: 'Supplier Name', type: 'text', required: true, maxLength: 255, minLength: 2},
        {name: 'notes', label: 'Supplier Notes', type: 'text', required: false, maxLength: 500, minLength: 0}
    ];

    return (
        <Page>
            <h1 className="h3 mb-2 text-gray-800 text-center">Suppliers</h1>
            <p className="mb-4 text-center">
                Suppliers are companies or individuals used to acquire materials for work orders and must be specified in purchases.
            </p>
            <Table fields={fields} name='Supplier' route='/supplier/' />
        </Page>
    )
}

export default Supplier;
