import InventoryTable from '../components/reusable/InventoryTable';
import Page from '../components/reusable/Page';
import { materialAPI } from '../api';

function Material() {
    const heading = 'Materials Inventory';
    const text = 'Current stock levels and unit costs for all materials';

    const fields = [
        {name: 'name', label: 'Material Name'},
        {name: 'description', label: 'Description'},
        {name: 'size', label: 'Size'}
    ];

    const extraFields = [
        {name: 'unit_cost', label: 'Unit Cost'},
        {name: 'available_quantity', label: 'In Stock'}
    ];

    return (
        <Page heading={heading} text={text}>
            <InventoryTable apiFunc={materialAPI.getMaterials} fields={fields} extraFields={extraFields} />
        </Page>
    );
};

export default Material;
