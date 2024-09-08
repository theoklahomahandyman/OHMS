import Table from '../components/reusable/Table';
import Page from '../components/reusable/Page';

function Supplier() {
    const fields = [
        {name: 'name', label: 'Supplier Name', type: 'text', required: true, elementType: 'input', maxLength: 255, minLength: 2},
        {name: 'notes', label: 'Supplier Notes', type: 'text', required: false, elementType: 'input', maxLength: 500, minLength: 0}
    ];

    const locationFields = [
        {name: 'street_address', label: 'Street Address', type: 'text', required: true, elementType: 'input', maxLength: 255, minLength: 2},
        {name: 'city', label: 'City', type: 'text', required: true, elementType: 'input', maxLength: 100, minLength: 2},
        {name: 'state', label: 'State', type: 'text', required: true, elementType: 'input', maxLength: 13, minLength: 2},
        {name: 'zip', label: 'Zip Code', type: 'number', required: true, elementType: 'input' },
        {name: 'notes', label: 'Notes', type: 'text', required: false, elementType: 'input', maxLength: 500 },
    ];

    const formsets = [
        {entity: 'Location', route: '/supplier/addresses/', fields: locationFields}
    ]

    return (
        <Page>
            <h1 className="h3 mb-2 text-gray-800 text-center">Suppliers</h1>
            <p className="mb-4 text-center">
                Suppliers are companies or individuals used to acquire materials for work orders and must be specified in purchases.
            </p>
            <Table fields={fields} name='Supplier' route='/supplier/' formsets={formsets} />
        </Page>
    )
}

export default Supplier;
