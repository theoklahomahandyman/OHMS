import { useState, useEffect, useCallback } from 'react';
import Loading from '../components/reusable/Loading';
import Form from '../components/reusable/form/Form';
import Page from '../components/reusable/Page';
import { useParams } from 'react-router-dom';
import { useNavigate } from 'react-router';
import { toast } from 'react-toastify';
import api from '../api';

function EditAsset() {
    const [assets, setAssets] = useState(false);
    const [loading, setLoading] = useState(false);
    const [data, setData] = useState({});

    const navigate = useNavigate();
    const { id } = useParams();
    const baseRoute = '/asset/';
    const updateRoute = `${baseRoute}${id}/`;

    const assetID = `OHMS-${id}-ASS`;
    const heading = `Edit Asset ${assetID}`;
    const text = `Please use this page to edit any information relating to asset ${assetID}, including maintenance events.`;

    const fetchData = useCallback(async () => {
        setLoading(true);
        try {
            const response = await api.get(updateRoute);
            setData(response.data || {});
        } catch {
            setData({});
        } finally {
            setLoading(false);
        }
    }, [updateRoute]);

    useEffect(() => {
        fetchData();
    }, [fetchData]);

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

    const handleSuccess = () => {
        navigate('/asset/');
        toast.success('Asset successfully updated!');
    };

    const conditionChoices = [
        { value: 'Good', label: 'Good' },
        { value: 'Maintenance Scheduled', label: 'Maintenance Scheduled' },
        { value: 'Maintenance Soon', label: 'Maintenance Soon' },
        { value: 'Needs Maintenance', label: 'Needs Maintenance' },
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
        {name: 'notes', label: 'Notes', type: 'text', required: false, elementType: 'input', maxLength: 500, minLength: 0}
    ];

    const formsets = [
        {entity: 'Instance', route: '/asset/instance/', fields: instanceFields},
    ]

    return (
        <Page heading={heading} text={text}>
            {loading ? <Loading /> : (
                <Form method='patch' route={updateRoute} baseRoute={baseRoute} initialData={data} buttonText='Save' buttonStyle='success' onSuccess={handleSuccess} fields={fields} formsets={formsets} id={id} fetchData={fetchData} />
            )}
        </Page>
    )
}

export default EditAsset;
