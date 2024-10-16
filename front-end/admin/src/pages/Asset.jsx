import Table from '../components/reusable/Table';
import Page from '../components/reusable/Page';
import { useState, useEffect } from 'react';
import { toast } from 'react-toastify';
import api from '../api';

function Asset() {
    const [assets, setAssets] = useState([]);

    const heading = 'Assets';

    const text = 'Assets are machinary purchased and when used in an order incurs an hourly usage charge.';

    useEffect(() => {
        async function fetchAssets() {
            try {
                const response = await api.get('/asset/');
                setAssets(response.data);
            } catch {
                toast.error('No Assets Found!');
            }
        }
        fetchAssets();
    }, []);

    const conditionChoices = [
        { value: 'Good', label: 'Good' },
        { value: 'Maintenance Scheduled', label: 'Maintenance Scheduled' },
        { value: 'Maintenance Soon', label: 'Maintenance Soon' },
        { value: 'Needs Maintenance', label: 'Needs Maintenance' },
        { value: 'Out of Service', label: 'Out of Service' },
    ];

    const statusChoices = [
        { value: 'Available', label: 'Available' },
        { value: 'In Use', label: 'In Use' },
        { value: 'Under Maintenance', label: 'Under Maintenance' },
        { value: 'Out of Service', label: 'Out of Service' },
    ];

    const fields = [
        {name: 'name', label: 'Name', type: 'text', required: true, elementType: 'input', maxLength: 255, minLength: 2},
        {name: 'description', label: 'Description', type: 'text', required: false, elementType: 'input', maxLength: 500, minLength: 0},
        {name: 'notes', label: 'Notes', type: 'text', required: false, elementType: 'input', maxLength: 500, minLength: 0}
    ];

    const instanceFields = [
        {name: 'asset', label: 'Asset', required: true, elementType: 'select', data: assets.map(asset => ({ value: asset.id, label: asset.name }))},
        {name: 'serial_number', label: 'Serial Number', type: 'text', required: true, elementType: 'input', maxLength: 100},
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

    const formsets = [
        {entity: 'Instance', route: '/asset/instance/', fields: instanceFields}
    ]

    return (
        <Page heading={heading} text={text}>
            <Table fields={fields} name='Asset' route='/asset/' formsets={formsets} />
        </Page>
    )
}

export default Asset;
