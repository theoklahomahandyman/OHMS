import PieChart from '../components/reusable/chart/PieChart';
import BarChart from '../components/reusable/chart/BarChart';
import { useState, useEffect, useCallback } from 'react';
import Loading from '../components/reusable/Loading';
import Page from '../components/reusable/Page';
import Form from '../components/reusable/form/Form';
import { useParams } from 'react-router-dom';
import { useNavigate } from 'react-router';
import { toast } from 'react-toastify';
import api from '../api';

function EditPurchase() {
    const [suppliers, setSuppliers] = useState([]);
    const [addresses, setAddresses] = useState([]);
    const [materials, setMaterials] = useState([]);
    const [loading, setLoading] = useState(false);
    const [data, setData] = useState({});
    const [pieChartData, setPieChartData] = useState({});
    const [barChartData, setBarChartData] = useState({});

    const navigate = useNavigate();
    const { id } = useParams();
    const baseRoute = '/purchase/'
    const updateRoute = `${baseRoute}${id}/`;

    const purchaseID = `OHMS-${id}-PUR`;
    const heading = `Edit Purchase ${purchaseID}`;
    const text = `Please use this page to edit any information relating to purchase order ${purchaseID}, including adding materials purchased. The cost field when adding a material should be the total amount spent on the selected material alone. The unit cost, inventory level, and total fields will update automatically.`;

    const fetchData = useCallback(async () => {
        const fetchMaterialDetail = async (purchase_id, material_id) => {
            const response = await api.get(`/purchase/material/${purchase_id}/${material_id}/`);
            return { name: response.data.name, cost: response.data.cost };
        };
        const updateChartData = async (purchaseData) => {
            const materialData = purchaseData.materials || [];
            const fetchedMaterials = await Promise.all(
                materialData.map(material_id => fetchMaterialDetail(purchaseData.id, material_id))
            ) || [];
            const materialNames = fetchedMaterials.map(m => m.name);
            const materialCosts = fetchedMaterials.map(m => m.cost);
            const taxAmount = purchaseData.tax || 0;
            if (taxAmount > 0) {
                materialNames.push('Tax');
                materialCosts.push(taxAmount);
            }
            setPieChartData({
                position: 'bottom',
                title: 'Purchase Charges',
                labels: materialNames,
                datasets: [{ label: 'Costs', data: materialCosts, offset: 20 }],
            });
            setBarChartData({
                position: 'bottom',
                title: 'Purchase Charges',
                labels: materialNames,
                datasets: [{ label: 'Costs', data: materialCosts, offset: 20 }],
            });
        };
        setLoading(true);
        try {
            const response = await api.get(updateRoute);
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
                const response = await api.get('/supplier/');
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
                const response = await api.get('/material/');
                setMaterials(response.data);
            } catch {
                toast.error('No Materials Found!');
            }
        }
        fetchMaterials();
    }, []);

    useEffect(() => {
        const fetchSupplierAddresses = async () => {
            if (data.supplier) {
                try {
                    const response = await api.get(`/supplier/addresses/${data.supplier}`);
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
                const response = await api.get(`/supplier/addresses/${supplier}`);
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

    const fields = [
        {name: 'supplier', label: 'Supplier', required: true, elementType: 'select', data: suppliers.map(supplier => ({ value: supplier.id, label: supplier.name })), customChange: handleSupplierChange, route: 'supplier/name'},
        {name: 'supplier_address', label: 'Supplier Address', required: true, elementType: 'select', data: addresses.map(address => ({ value: address.id, label: `${address.street_address} ${address.city}, ${address.state} ${address.zip}` })), route: '/supplier/address'},
        {name: 'tax', label: 'Tax Amount', required: false, elementType: 'input', type: 'number', minValue: 0.00},
        {name: 'total', label: 'Total Amount', required: false, elementType: 'input', type: 'number', minValue: 0.00, disabled: true},
        {name: 'date', label: 'Date', required: true, elementType: 'input', type: 'date'},
        {name: 'uploaded_images', label: 'Reciept', required: false, elementType: 'input', type: 'file'},
    ];

    const materialFields = [
        {name: 'material', label: 'Material', required: true, elementType: 'select', data: materials.map(material => ({ value: material.id, label: material.name }))},
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

    const formsets = [
        {entity: 'Material', route: '/purchase/material/', fields: materialFields, newEntity: false},
        {entity: 'Material', route: '/purchase/new/material/', fields: newMaterialFields, newEntity: true},
    ];

    return (
        <Page heading={heading} text={text}>
            {loading ? <Loading /> : (
                <>
                    <div className="row justify-content-center">
                        <div className="col-auto">
                            <PieChart chartData={pieChartData} />
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
