import InventoryTable from '../components/reusable/InventoryTable';
import Page from '../components/reusable/Page';
import { toolAPI } from '../api';

function Tool() {
    const heading = 'Tools Inventory';
    const text = 'Current stock levels and unit costs for all tools';

    const fields = [
        {name: 'name', label: 'Tool Name'},
        {name: 'description', label: 'Description'},
    ];

    const extraFields = [
        {name: 'unit_cost', label: 'Unit Cost'},
        {name: 'available_quantity', label: 'In Stock'}
    ];

    return (
        <Page heading={heading} text={text}>
            <InventoryTable apiFunc={toolAPI.getTools} fields={fields} extraFields={extraFields} />
        </Page>
    );
};

export default Tool;
