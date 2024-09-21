import Table from '../components/reusable/Table';
import Page from '../components/reusable/Page';

function Material() {
    const heading = 'Materials';

    const text = 'Materials are used in both work orders and purchases. They must be created here before being added to a work order or purchase.';

    const fields = [
        {name: 'name', label: 'Material Name', type: 'text', required: true, elementType: 'input', maxLength: 255, minLength: 2},
        {name: 'description', label: 'Material Description', type: 'text', required: false, elementType: 'input', maxLength: 500, minLength: 0},
        {name: 'size', label: 'Material Size', type: 'text', required: true, elementType: 'input', maxLength: 255, minLength: 2}
    ];

    const extraFields = [
        {name: 'unit_cost', label: 'Unit Cost'},
        {name: 'available_quantity', label: 'Available Quantity'}
    ];

    return (
        <Page heading={heading} text={text}>
            <Table fields={fields} name='Material' route='/material/' extraFields={extraFields} />
        </Page>
    )
}

export default Material;
