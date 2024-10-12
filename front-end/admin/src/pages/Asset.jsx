import Table from '../components/reusable/Table';
import Page from '../components/reusable/Page';

function Asset() {
    const heading = 'Assets';

    const text = 'Assets are machinary purchased and when used in an order incurs an hourly usage charge.';

    const conditionChoices = [
        { value: 'good', label: 'Good' },
        { value: 'needs maintenance', label: 'Needs Maintenance' },
        { value: 'out of service', label: 'Out of Service' },
    ];

    const statusChoices = [
        { value: 'available', label: 'Available' },
        { value: 'in use', label: 'In Use' },
        { value: 'under maintenance', label: 'Under Maintenance' },
        { value: 'out of service', label: 'Out of Service' },
    ];

    const fields = [
        {name: 'name', label: 'Name', type: 'text', required: true, elementType: 'input', maxLength: 255, minLength: 2},
        {name: 'serial_number', label: 'Serial Number', type: 'text', required: true, elementType: 'input', maxLength: 100},
        {name: 'description', label: 'Description', type: 'text', required: false, elementType: 'input', maxLength: 500, minLength: 0},
        {name: 'unit_cost', label: 'Cost', type: 'number', required: false, elementType: 'input', disabled: true},
        {name: 'rental_cost', label: 'Rental Charge', type: 'number', required: false, elementType: 'input'},
        {name: 'last_maintenance', label: 'Last Maintenance', type: 'date', required: false, elementType: 'input'},
        {name: 'next_maintenance', label: 'Next Maintenance', type: 'date', required: false, elementType: 'input'},
        {name: 'usage', label: 'Usage', type: 'number', required: false, elementType: 'input'},
        {name: 'location', label:  'Stored Location', type: 'text', required: false, elementType: 'input'},
        {name: 'condition', label: 'Current Condition', elementType: 'select', data: conditionChoices},
        {name: 'status', label: 'Current Status', elementType: 'select', data: statusChoices},
        {name: 'notes', label: 'Notes', type: 'text', required: false, elementType: 'input', maxLength: 500, minLength: 0}
    ];

    const maintenanceFields = [
        {name: 'date', label: 'Date', type: 'date', required: true, elementType: 'input'},
        {name: 'next_maintenance', label: 'Next Maintenance', type: 'date', required: true, elementType: 'input'},
        {name: 'current_usage', label: 'Current Usage', type: 'number', required: true, elementType: 'input'},
        {name: 'condition', label: 'New Condition', required: true, elementType: 'select', data: conditionChoices},
        {name: 'status', label: 'New Status', required: true, elementType: 'select', data: statusChoices},
        {name: 'notes', label: 'Notes', type: 'text', required: false, elementType: 'input', maxLength: 500, minLength: 0}
    ];

    const formsets = [
        {entity: 'Maintenance', route: '/asset/maintenance/', fields: maintenanceFields}
    ]

    return (
        <Page heading={heading} text={text}>
            <Table fields={fields} name='Asset' route='/asset/' formsets={formsets} />
        </Page>
    )
}

export default Asset;
