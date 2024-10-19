import { useState, useEffect, useCallback } from 'react';
import Loading from '../components/reusable/Loading';
import Page from '../components/reusable/Page';
import Form from '../components/reusable/form/Form';
import { useParams } from 'react-router-dom';
import { useNavigate } from 'react-router';
import { toast } from 'react-toastify';
import api from '../api';

function EditOrder() {
    const [customers, setCustomers] = useState([]);
    const [services, setServices] = useState([]);
    const [materials, setMaterials] = useState([]);
    const [tools, setTools] = useState([]);
    const [assets, setAssets] = useState([]);
    const [users, setUsers] = useState([]);
    const [loading, setLoading] = useState(false);
    const [data, setData] = useState({});

    const navigate = useNavigate();
    const { id } = useParams();
    const baseRoute = '/order/';
    const updateRoute = `${baseRoute}${id}/`;

    const orderID = `OHMS-${id}-ORD`;
    const heading = `Edit Order ${orderID}`;
    const text = `Please use this page to edit any information relating to order ${orderID}, including adding materials used, line item costs, and payments. The inventory level for materials, paid, and total fields will update automatically.`;

    const calloutChoices = [
        { value: '50.0', label: 'Standard - $50.00' },
        { value: '175.0', label: 'Emergency - $175.00' },
    ];

    const paymentChoices = [
        { value: 'cash', label: 'Cash' },
        { value: 'check', label: 'Check' },
    ];

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
        async function fetchCustomers() {
            try {
                const response = await api.get('/customer/');
                setCustomers(response.data);
            } catch {
                toast.error('No Customers Found!');
            }
        }
        fetchCustomers();
    }, []);

    useEffect(() => {
        async function fetchServices() {
            try {
                const response = await api.get('/service/');
                setServices(response.data);
            } catch {
                toast.error('No Services Found!');
            }
        }
        fetchServices();
    }, []);

    useEffect(() => {
        async function fetchMaterials() {
            try {
                const response = await api.get('/material/');
                setMaterials(response.data);
            } catch {
                toast.error('No Materials Found!');
            }
        }
        fetchMaterials();
    }, []);

    useEffect(() => {
        async function fetchTools() {
            try {
                const response = await api.get('/tool/');
                setTools(response.data);
            } catch {
                toast.error('No Tools Found!');
            }
        }
        fetchTools();
    }, []);

    useEffect(() => {
        async function fetchAssets() {
            try {
                const response = await api.get('/asset/instance/');
                setAssets(response.data);
            } catch {
                toast.error('No Assets Found!');
            }
        }
        fetchAssets();
    }, []);

    useEffect(() => {
        async function fetchUsers() {
            try {
                const response = await api.get('/user/admin/');
                setUsers(response.data);
            } catch {
                toast.error('No Users Found!');
            }
        }
        fetchUsers()
    }, []);

    const handleSuccess = () => {
        navigate('/order/');
        toast.success('Order successfully updated!');
    }

    const conditionChoices = [
        { value: 'Good', label: 'Good' },
        { value: 'Maintenance Scheduled', label: 'Maintenance Scheduled' },
        { value: 'Maintenance Soon', label: 'Maintenance Soon' },
        { value: 'Needs Maintenance', label: 'Needs Maintenance' },
        { value: 'Out of Service', label: 'Out of Service' },
    ];

    const fields = [
        {name: 'customer', label: 'Customer', required: true, elementType: 'select', data: customers.map(customer => ({ value: customer.id, label: `${customer.first_name} ${customer.last_name}` })), route: '/customer/name'},
        {name: 'date', label: 'Date', required: true, elementType: 'input', type: 'date'},
        {name: 'service', label: 'Service', required: true, elementType: 'select', data: services.map(service => ({ value: service.id, label: service.name })), route: '/service/name'},
        {name: 'completed', label: 'Complete', required: false, elementType: 'input', type: 'checkbox'},
        {name: 'paid', label: 'Paid', required: false, elementType: 'input', type: 'checkbox', disabled: true},
        {name: 'discount', label: 'Discount (%)', required: false, elementType: 'input', type: 'number', minValue: 0.00, maxValue: 100.0},
        {name: 'discount_total', label: 'Discount Total ($)', required: false, elementType: 'input', type: 'number', minValue: 0.00, disabled: true},
        {name: 'callout', label: 'Callout Type', required: false, elementType: 'select', data: calloutChoices},
        {name: 'uploaded_images', label: 'Pictures', required: false, elementType: 'input', type: 'file'},
        {name: 'hourly_rate', label: 'Hourly Rate ($)', required: false, elementType: 'input', type: 'number', minValue: 75.0},
        {name: 'hours_worked', label: 'Hours Worked', required: false, elementType: 'input', type: 'number', minValue: 3.0, disabled: true},
        {name: 'labor_total', label: 'Labor Total ($)', required: false, elementType: 'input', type: 'number', minValue: 0.00, disabled: true},
        {name: 'line_total', label: 'Line Item Total ($)', required: false, elementType: 'input', type: 'number', minValue: 0.00, disabled: true},
        {name: 'material_upcharge', label: 'Material Upcharge (%)', required: false, elementType: 'input', type: 'number', minValue: 15.0, maxValue: 75.0},
        {name: 'material_total', label: 'Material Total ($)', required: false, elementType: 'input', type: 'number', minValue: 0.00, disabled: true},
        {name: 'tax', label: 'Tax (%)', required: false, elementType: 'input', type: 'number', minValue: 0.00, maxValue: 20.0},
        {name: 'tax_total', label: 'Tax Total ($)', required: false, elementType: 'input', type: 'number', minValue: 0.00, disabled: true},
        {name: 'subtotal', label: 'Subtotal ($)', required: false, elementType: 'input', type: 'number', minValue: 0.00, disabled: true},
        {name: 'total', label: 'Total ($)', required: false, elementType: 'input', type: 'number', minValue: 0.00, disabled: true},
        {name: 'payment_total', label: 'Payment Total ($)', required: false, elementType: 'input', type: 'number', minValue: 0.00, disabled: true},
        {name: 'working_total', label: 'Total Due ($)', required: false, elementType: 'input', type: 'number', minValue: 0.00, disabled: true},
        {name: 'description', label: 'Description', type: 'text', required: false, elementType: 'input', maxLength: 2000},
        {name: 'notes', label: 'Notes', type: 'text', required: false, elementType: 'input', maxLength: 10000},
    ];

    const costFields = [
        {name: 'name', label: 'Name', type: 'text', required: true, elementType: 'input', minLength: 2, maxLength: 300},
        {name: 'cost', label: 'Cost ($)', type: 'number', required: true, elementType: 'input', minValue: 0.0},
    ];

    const materialFields = [
        {name: 'material', label: 'Material', required: true, elementType: 'select', data: materials.map(material => ({ value: material.id, label: material.name }))},
        {name: 'quantity', label: 'Quantity', type: 'number', required: true, elementType: 'input'},
    ];

    const toolFields = [
        {name: 'tool', label: 'Tool', required: true, elementType: 'select', data: tools.map(tool => ({ value: tool.id, label: tool.name }))},
        {name: 'quantity_used', label: 'Quantity Needed', type: 'number', required: true, elementType: 'input'},
        {name: 'quantity_broken', label: 'Quantity Broken', type: 'number', required: true, elementType: 'input'},
    ];

    const assetFields = [
        {name: 'instance', label: 'Asset', required: true, elementType: 'select', data: assets.map(asset => ({ value: asset.id, label: asset.asset.name }))},
        {name: 'usage', label: 'Usage', type: 'number', required: true, elementType: 'input'},
        {name: 'condition', label: 'Current Condition', elementType: 'select', data: conditionChoices},
    ];

    const paymentFields = [
        {name: 'date', label: 'Date', required: true, elementType: 'input', type: 'date'},
        {name: 'type', label: 'Payment Type', required: true, elementType: 'select', data: paymentChoices},
        {name: 'total', label: 'Total ($)', required: true, elementType: 'input', type: 'number', minValue: 0.00},
        {name: 'notes', label: 'Notes', required: false, elementType: 'input', type: 'text', maxLength: 255},
    ];

    const workerFields = [
        {name: 'user', label: 'Worker', required: true, elementType: 'select',  data: users.map(user => ({ value: user.id, label: `${user.first_name} ${user.last_name}`}))},
        {name: 'total', label: 'Pay ($)', required: false, elementType: 'input', type: 'number', disabled: true}
    ];

    const workLogFields = [
        {name: 'start', label: 'Start Time', required: true, elementType: 'input', type: 'datetime-local'},
        {name: 'end', label: 'End Time', required: true, elementType: 'input', type: 'datetime-local'},
    ];

    const formsets = [
        {entity: 'Line Item Cost', route: '/order/cost/', fields: costFields, newEntity: false},
        {entity: 'Material', route: '/order/material/', fields: materialFields, newEntity: false},
        {entity: 'Tool', route: '/order/tool/', fields: toolFields, newEntity: false},
        {entity: 'Asset', route: '/order/asset/', fields: assetFields, newEntity: false},
        {entity: 'Work Log', route: '/order/worklog/', fields: workLogFields, newEntity: false},
        {entity: 'Payment', route: '/order/payment/', fields: paymentFields, newEntity: false},
        {entity: 'Worker', route: '/order/worker/', fields: workerFields, newEntity: false},
    ];

    return (
        <Page heading={heading} text={text}>
            {loading ? <Loading /> : (
                <Form method='patch' route={updateRoute} baseRoute={baseRoute} initialData={data} fetchData={fetchData} initialFiles={{images: data['images']}} buttonText='Save' buttonStyle='success' onSuccess={handleSuccess} fields={fields} formsets={formsets} id={id} />
            )}
        </Page>
    )
}

export default EditOrder;
