import PieChart from '../components/reusable/chart/PieChart';
import BarChart from '../components/reusable/chart/BarChart';
import { useState, useEffect, useCallback } from 'react';
import Loading from '../components/reusable/Loading';
import Page from '../components/reusable/Page';
import Form from '../components/reusable/form/Form';
import { useParams } from 'react-router-dom';
import { useNavigate } from 'react-router';
import { toast } from 'react-toastify';
import { makeRequest } from '../api';

function EditOrder() {
    const [customers, setCustomers] = useState([]);
    const [services, setServices] = useState([]);
    const [materials, setMaterials] = useState([]);
    const [tools, setTools] = useState([]);
    // const [assets, setAssets] = useState([]);
    const [users, setUsers] = useState([]);
    const [loading, setLoading] = useState(false);
    const [data, setData] = useState({});
    const [totalPieChartData, setTotalPieChartData] = useState({});
    const [totalBarChartData, setTotalBarChartData] = useState({});
    const [toolBarChartData, setToolBarChartData] = useState({});
    const [costPieChartData, setCostPieChartData] = useState({});
    const [materialPieChartData, setMaterialPieChartData] = useState({});

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
        const fetchMaterialDetail = async (order_id, material_id) => {
            const response = await makeRequest('get', `/order/material/${order_id}/${material_id}/`);
            return { name: response.data.name, cost: response.data.cost, quantity: response.data.quantity };
        };
        const fetchToolDetail = async (order_id, tool_id) => {
            const response = await makeRequest('get', `/order/tool/${order_id}/${tool_id}/`);
            return { name: response.data.name, quantity_used: response.data.quantity_used, quantity_broken: response.data.quantity_broken };
        };
        const fetchCostDetail = async (order_id, cost_id) => {
            const response = await makeRequest('get', `/order/cost/${order_id}/${cost_id}/`);
            return { name: response.data.name, cost: response.data.cost };
        };
        const updateChartData = async (orderData) => {
            const materialData = orderData.materials || [];
            const toolData = orderData.tools || [];
            const costData = orderData.costs || [];
            const fetchedMaterials = await Promise.all(
                materialData.map(material => fetchMaterialDetail(orderData.id, material.id))
            ) || [];
            const fetchedTools = await Promise.all(
                toolData.map(tool => fetchToolDetail(orderData.id, tool.id))
            ) || [];
            const fetchedCosts = await Promise.all(
                costData.map(cost => fetchCostDetail(orderData.id, cost.id))
            ) || [];
            const materialNames = fetchedMaterials.map(m => m.name);
            const materialCosts = fetchedMaterials.map(m => m.cost);
            const materialQuantities = fetchedMaterials.map(m => m.quantity);
            const toolNames = fetchedTools.map(t => t.name);
            const toolQuantityUsed = fetchedTools.map(t => t.quantity_used);
            const toolQuantityBroken = fetchedTools.map(t => t.quantity_broken);
            const lineNames = fetchedCosts.map(c => c.name);
            const lineCosts = fetchedCosts.map(c => c.cost);
            const taxTotal = orderData.tax_total || 0;
            const laborTotal = orderData.labor_total || 0;
            const materialTotal = orderData.material_total || 0;
            const lineTotal = orderData.line_total || 0;
            const calloutTotal = orderData.callout;
            const allChargeNames = ['Callout Charge', 'Labor Charge', 'Material Charges', 'Line Item Charges', 'Tax Charge'];
            const allChargeCosts = [calloutTotal, laborTotal, materialTotal, lineTotal, taxTotal];
            setMaterialPieChartData({
                position: 'bottom',
                title: 'Material Charges',
                labels: materialNames,
                datasets: [{ label: 'Charges', data: materialCosts, offset: 20 }, { label: 'Quantities', data: materialQuantities, offset: 20 }],
            });
            setToolBarChartData({
                position: 'bottom',
                title: 'Tools Used and Broken',
                labels: toolNames,
                datasets: [{ label: 'Quantities Used', data: toolQuantityUsed, offset: 20 }, { label: 'Quantities Broken', data: toolQuantityBroken, offset: 20 }],
            });
            setCostPieChartData({
                position: 'bottom',
                title: 'Line Item Charges',
                labels: lineNames,
                datasets: [{ label: 'Charges', data: lineCosts, offset: 20 }],
            });
            setTotalPieChartData({
                position: 'bottom',
                title: 'Total Charges',
                labels: allChargeNames,
                datasets: [{ label: 'Charges', data: allChargeCosts, offset: 20 }],
            });
            setTotalBarChartData({
                position: 'bottom',
                title: 'Total Charges',
                labels: allChargeNames,
                datasets: [{ label: 'Charges', data: allChargeCosts, offset: 20 }],
            });
        }
        setLoading(true);
        try {
            const response = await makeRequest('get', updateRoute);
            setData(response.data || {});
            await updateChartData(response.data);
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
                const response = await makeRequest('get', '/customer/');
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
                const response = await makeRequest('get', '/service/');
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
                const response = await makeRequest('get', '/material/');
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
                const response = await makeRequest('get', '/tool/');
                setTools(response.data);
            } catch {
                toast.error('No Tools Found!');
            }
        }
        fetchTools();
    }, []);

    // useEffect(() => {
    //     async function fetchAssets() {
    //         try {
    //             const response = await api.get('/asset/instance/');
    //             setAssets(response.data);
    //         } catch {
    //             toast.error('No Assets Found!');
    //         }
    //     }
    //     fetchAssets();
    // }, []);

    useEffect(() => {
        async function fetchUsers() {
            try {
                const response = await makeRequest('get', '/user/admin/');
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

    // const conditionChoices = [
    //     { value: 'Good', label: 'Good' },
    //     { value: 'Maintenance Scheduled', label: 'Maintenance Scheduled' },
    //     { value: 'Maintenance Soon', label: 'Maintenance Soon' },
    //     { value: 'Needs Maintenance', label: 'Needs Maintenance' },
    //     { value: 'Out of Service', label: 'Out of Service' },
    // ];

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
        {name: 'inventory_item', label: 'Material', required: true, elementType: 'select', data: materials.map(material => ({ value: material.id, label: material.name }))},
        {name: 'quantity', label: 'Quantity', type: 'number', required: true, elementType: 'input'},
    ];

    const toolFields = [
        {name: 'inventory_item', label: 'Tool', required: true, elementType: 'select', data: tools.map(tool => ({ value: tool.id, label: tool.name }))},
        {name: 'quantity', label: 'Quantity Needed', type: 'number', required: true, elementType: 'input'},
        {name: 'quantity_broken', label: 'Quantity Broken', type: 'number', required: false, elementType: 'input'},
    ];

    // const assetFields = [
    //     {name: 'instance', label: 'Asset', required: true, elementType: 'select', data: assets.map(asset => ({ value: asset.id, label: asset.asset.name }))},
    //     {name: 'usage', label: 'Usage', type: 'number', required: true, elementType: 'input'},
    //     {name: 'condition', label: 'Current Condition', elementType: 'select', data: conditionChoices},
    // ];

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
        // {entity: 'Asset', route: '/order/asset/', fields: assetFields, newEntity: false},
        {entity: 'Work Log', route: '/order/worklog/', fields: workLogFields, newEntity: false},
        {entity: 'Payment', route: '/order/payment/', fields: paymentFields, newEntity: false},
        {entity: 'Worker', route: '/order/worker/', fields: workerFields, newEntity: false},
    ];

    return (
        <Page heading={heading} text={text}>
            {loading ? <Loading /> : (
                <>
                    <div className="row justify-content-center">
                        <div className="col-auto">
                            <PieChart chartData={materialPieChartData} />
                        </div>
                        <div className="col-auto">
                            <PieChart chartData={toolBarChartData} />
                        </div>
                        <div className="col-auto">
                            <PieChart chartData={costPieChartData} />
                        </div>
                        <div className="col-auto">
                            <PieChart chartData={totalPieChartData} />
                        </div>
                        <div className="col-auto">
                            <BarChart chartData={totalBarChartData} />
                        </div>
                    </div>
                    <Form method='patch' route={updateRoute} baseRoute={baseRoute} initialData={data} fetchData={fetchData} initialFiles={{images: data['images']}} buttonText='Save' buttonStyle='success' onSuccess={handleSuccess} fields={fields} formsets={formsets} id={id} />
                </>
            )}
        </Page>
    )
}

export default EditOrder;
