import PieChart from '../components/reusable/chart/PieChart';
import BarChart from '../components/reusable/chart/BarChart';
import { useState, useEffect, useCallback } from 'react';
import Loading from '../components/reusable/Loading';
import Form from '../components/reusable/form/Form';
import Page from '../components/reusable/Page';
import { useParams } from 'react-router-dom';
import { useNavigate } from 'react-router';
import { toast } from 'react-toastify';
import { makeRequest } from '../api';

function EditPurchase() {
    const [suppliers, setSuppliers] = useState([]);
    const [addresses, setAddresses] = useState([]);
    const [materials, setMaterials] = useState([]);
    const [tools, setTools] = useState([]);
    // const [assets, setAssets] = useState([]);
    const [loading, setLoading] = useState(false);
    const [data, setData] = useState({});
    const [materialPieChartData, setMaterialPieChartData] = useState({});
    const [toolPieChartData, setToolPieChartData] = useState({});
    // const [assetPieChartData, setAssetPieChartData] = useState({});
    const [totalPieChartData, setTotalPieChartData] = useState({});
    const [barChartData, setBarChartData] = useState({});

    const navigate = useNavigate();
    const { id } = useParams();
    const baseRoute = '/purchase/'
    const updateRoute = `${baseRoute}${id}/`;

    const purchaseID = `OHMS-${id}-PUR`;
    const heading = `Edit Purchase ${purchaseID}`;
    const text = `Please use this page to edit any information relating to purchase order ${purchaseID}, including adding materials, tools, and assets purchased. The cost field when adding a material or tool should be the total amount spent on the selected material or tool alone. The unit cost, inventory level, and total fields will update automatically.`;

    const fetchData = useCallback(async () => {
        const fetchMaterialDetail = async (purchase_id, material_id) => {
            const response = await makeRequest('get', `/purchase/material/${purchase_id}/${material_id}/`);
            return { name: response.data.name, cost: response.data.cost, quantity: response.data.quantity };
        };
        const fetchToolDetail = async (purchase_id, tool_id) => {
            const response = await makeRequest('get', `/purchase/tool/${purchase_id}/${tool_id}/`);
            return { name: response.data.name, cost: response.data.cost, quantity: response.data.quantity };
        };
        // const fetchAssetDetail = async (purchase_id, asset_id) => {
        //     const response = await api.get(`/purchase/asset/${purchase_id}/${asset_id}/`);
        //     return { name: response.data.asset_name, cost: response.data.cost, quantity: 1 };
        // };
        const updateChartData = async (purchaseData) => {
            const materialData = purchaseData.materials || [];
            const toolData = purchaseData.tools || [];
            // const assetData = purchaseData.assets || [];
            const fetchedMaterials = await Promise.all(
                materialData.map(material => fetchMaterialDetail(purchaseData.id, material.id))
            ) || [];
            const fetchedTools = await Promise.all(
                toolData.map(tool => fetchToolDetail(purchaseData.id, tool.id))
            ) || [];
            // const fetchedAssets = await Promise.all(
            //     assetData.map(asset => fetchAssetDetail(purchaseData.id, asset.id))
            // ) || [];
            const materialNames = fetchedMaterials.map(m => m.name);
            const materialCosts = fetchedMaterials.map(m => m.cost);
            const materialQuantities = fetchedMaterials.map(m => m.quantity);
            const toolNames = fetchedTools.map(t => t.name);
            const toolCosts = fetchedTools.map(t => t.cost);
            const toolQuantities = fetchedTools.map(t => t.quantity);
            // const assetNames = fetchedAssets.map(a => a.name);
            // const assetCosts = fetchedAssets.map(a => a.cost);
            // const assetQuantities = fetchedAssets.map(a => a.quantity);
            const taxAmount = purchaseData.tax || 0;
            const allChargeNames = [...materialNames, ...toolNames, 'Tax'];
            const allChargeCosts = [...materialCosts, ...toolCosts, taxAmount];
            const allChargeQuantities = [...materialQuantities, ...toolQuantities, 0];
            setMaterialPieChartData({
                position: 'bottom',
                title: 'Material Charges',
                labels: materialNames,
                datasets: [{ label: 'Costs', data: materialCosts, offset: 20 }, { label: 'Quantities', data: materialQuantities, offset: 20 }],
            });
            setToolPieChartData({
                position: 'bottom',
                title: 'Tool Charges',
                labels: toolNames,
                datasets: [{ label: 'Costs', data: toolCosts, offset: 20 }, { label: 'Quantities', data: toolQuantities, offset: 20 }],
            });
            // setAssetPieChartData({
            //     position: 'bottom',
            //     title: 'Asset Purchase Charges',
            //     labels: assetNames,
            //     datasets: [{ label: 'Costs', data: assetCosts, offset: 20 }, {label: 'Quantities', data: assetQuantities, offset: 20 }],
            // });
            setTotalPieChartData({
                position: 'bottom',
                title: 'Total Charges',
                labels: allChargeNames,
                datasets: [{ label: 'Costs', data: allChargeCosts, offset: 20 }, {label: 'Quantities', data: allChargeQuantities, offset: 20 }],
            });
            setBarChartData({
                position: 'bottom',
                title: 'Total Charges and Quantities',
                labels: allChargeNames,
                datasets: [{ label: 'Costs', data: allChargeCosts, offset: 20 }, {label: 'Quantities', data: allChargeQuantities, offset: 20 }],
            });
        };
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
        async function fetchSuppliers() {
            try {
                const response = await makeRequest('get', '/supplier/');
                setSuppliers(response.data);
            } catch {
                toast.error('No Suppliers Found!');
            }
        }
        fetchSuppliers();
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
    //             const response = await api.get('/asset/');
    //             setAssets(response.data);
    //         } catch {
    //             toast.error('No Assets Found!');
    //         }
    //     }
    //     fetchAssets();
    // }, []);

    useEffect(() => {
        const fetchSupplierAddresses = async () => {
            if (data.supplier) {
                try {
                    const response = await makeRequest('get', `/supplier/addresses/${data.supplier}`);
                    setAddresses(response.data);
                } catch {
                    toast.error('No Addresses Found!');
                }
            }
        };
        fetchSupplierAddresses();
    }, [data.supplier])

    const handleSupplierChange = async (event) => {
        const supplier = event.target.value;
        setAddresses([])
        if (supplier) {
            try {
                const response = await makeRequest('get', `/supplier/addresses/${supplier}`);
                setAddresses(response.data);
            } catch {
                toast.error('No Addresses Found!');
            }
        }
    }

    const handleSuccess = () => {
        navigate('/purchase/');
        toast.success('Purchase successfully updated!');
    }

    // const conditionChoices = [
    //     { value: 'Good', label: 'Good' },
    //     { value: 'Maintenance Scheduled', label: 'Maintenance Scheduled' },
    //     { value: 'Maintenance Soon', label: 'Maintenance Soon' },
    //     { value: 'Needs Maintenance', label: 'Needs Maintenance' },
    //     { value: 'Out of Service', label: 'Out of Service' },
    // ];

    const fields = [
        {name: 'supplier', label: 'Supplier', required: true, elementType: 'select', data: suppliers.map(supplier => ({ value: supplier.id, label: supplier.name })), customChange: handleSupplierChange, route: 'supplier/name'},
        {name: 'supplier_address', label: 'Supplier Address', required: true, elementType: 'select', data: addresses.map(address => ({ value: address.id, label: `${address.street_address} ${address.city}, ${address.state} ${address.zip}` })), route: '/supplier/address'},
        {name: 'date', label: 'Date', required: true, elementType: 'input', type: 'date'},
        {name: 'uploaded_images', label: 'Reciept', required: false, elementType: 'input', type: 'file'},
        {name: 'tax', label: 'Tax ($)', required: false, elementType: 'input', type: 'number', minValue: 0.00},
        {name: 'material_total', label: 'Material Total ($)', required: false, elementType: 'input', type: 'number', minValue: 0.00, disabled: true},
        {name: 'tool_total', label: 'Tool Total ($)', required: false, elementType: 'input', type: 'number', minValue: 0.00, disabled: true},
        // {name: 'asset_total', label: 'Asset Total ($)', required: false, elementType: 'input', type: 'number', minValue: 0.00, disabled: true},
        {name: 'subtotal', label: 'Subtotal ($)', required: false, elementType: 'input', type: 'number', minValue: 0.00, disabled: true},
        {name: 'total', label: 'Total ($)', required: false, elementType: 'input', type: 'number', minValue: 0.00, disabled: true},
    ];

    const materialFields = [
        {name: 'inventory_item', label: 'Material', required: true, elementType: 'select', data: materials.map(material => ({ value: material.id, label: material.name }))},
        {name: 'quantity', label: 'Quantity', type: 'number', required: true, elementType: 'input'},
        {name: 'cost', label: 'Cost', type: 'number', required: true, elementType: 'input'},
    ];

    const newMaterialFields = [
        {name: 'name', label: 'Material Name', type: 'text', required: true, elementType: 'input', maxLength: 255, minLength: 2},
        {name: 'description', label: 'Material Description', type: 'text', required: false, elementType: 'input', maxLength: 500, minLength: 0},
        {name: 'size', label: 'Material Size', type: 'text', required: true, elementType: 'input', maxLength: 255, minLength: 2},
        {name: 'quantity', label: 'Quantity', type: 'number', required: true, elementType: 'input'},
        {name: 'cost', label: 'Cost', type: 'number', required: true, elementType: 'input'},
    ];

    const toolFields = [
        {name: 'inventory_item', label: 'Tool', required: true, elementType: 'select', data: tools.map(tool => ({ value: tool.id, label: tool.name }))},
        {name: 'quantity', label: 'Quantity', type: 'number', required: true, elementType: 'input'},
        {name: 'cost', label: 'Cost', type: 'number', required: true, elementType: 'input'},
    ];

    const newToolFields = [
        {name: 'name', label: 'Tool Name', type: 'text', required: true, elementType: 'input', maxLength: 255, minLength: 2},
        {name: 'description', label: 'Tool Description', type: 'text', required: false, elementType: 'input', maxLength: 500, minLength: 0},
        {name: 'quantity', label: 'Quantity', type: 'number', required: true, elementType: 'input'},
        {name: 'cost', label: 'Cost', type: 'number', required: true, elementType: 'input'},
    ];

    // const assetFields = [
    //     {name: 'asset', label: 'Asset', required: true, elementType: 'select', data: assets.map(asset => ({ value: asset.id, label: asset.name }))},
    //     {name: 'serial_number', label: 'Serial Number', type: 'text', required: true, elementType: 'input', maxLength: 100},
    //     {name: 'cost', label: 'Cost', type: 'number', required: false, elementType: 'input'},
    //     {name: 'charge', label: 'Rental Charge', type: 'number', required: false, elementType: 'input'},
    //     {name: 'last_maintenance', label: 'Last Maintenance', type: 'date', required: false, elementType: 'input'},
    //     {name: 'next_maintenance', label: 'Next Maintenance', type: 'date', required: false, elementType: 'input'},
    //     {name: 'usage', label: 'Usage', type: 'number', required: false, elementType: 'input'},
    //     {name: 'condition', label: 'Current Condition', elementType: 'select', data: conditionChoices},
    // ];

    // const newAssetFields = [
    //     {name: 'name', label: 'Asset Name', type: 'text', required: true, elementType: 'input', maxLength: 255, minLength: 2},
    //     {name: 'description', label: 'Asset Description', type: 'text', required: false, elementType: 'input', maxLength: 500, minLength: 0},
    //     {name: 'serial_number', label: 'Serial Number', type: 'text', required: true, elementType: 'input', maxLength: 100},
    //     {name: 'cost', label: 'Cost', type: 'number', required: false, elementType: 'input'},
    //     {name: 'charge', label: 'Rental Charge', type: 'number', required: false, elementType: 'input'},
    //     {name: 'last_maintenance', label: 'Last Maintenance', type: 'date', required: false, elementType: 'input'},
    //     {name: 'next_maintenance', label: 'Next Maintenance', type: 'date', required: false, elementType: 'input'},
    //     {name: 'usage', label: 'Usage', type: 'number', required: false, elementType: 'input'},
    //     {name: 'condition', label: 'Current Condition', elementType: 'select', data: conditionChoices},
    // ];

    const formsets = [
        {entity: 'Material', route: '/purchase/material/', fields: materialFields, newEntity: false},
        {entity: 'Material', route: '/purchase/new/material/', fields: newMaterialFields, newEntity: true},
        {entity: 'Tool', route: '/purchase/tool/', fields: toolFields, newEntity: false},
        {entity: 'Tool', route: '/purchase/new/tool/', fields: newToolFields, newEntity: true},
        // {entity: 'Asset', route: '/purchase/asset/', fields: assetFields, newEntity: false},
        // {entity: 'Asset', route: '/purchase/new/asset/', fields: newAssetFields, newEntity: true},
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
                            <PieChart chartData={toolPieChartData} />
                        </div>
                        {/* <div className="col-auto">
                            <PieChart chartData={assetPieChartData} />
                        </div> */}
                        <div className="col-auto">
                            <PieChart chartData={totalPieChartData} />
                        </div>
                        <div className="col-auto">
                            <BarChart chartData={barChartData} />
                        </div>
                    </div>
                    <Form method='patch' route={updateRoute} baseRoute={baseRoute} initialData={data} initialFiles={{images: data['images']}} buttonText='Save' buttonStyle='success' onSuccess={handleSuccess} fields={fields} formsets={formsets} id={id} fetchData={fetchData} />
                </>
            )}
        </Page>
    )
}

export default EditPurchase;
