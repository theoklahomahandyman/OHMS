import { useState, useEffect, useCallback } from 'react';
import Loading from '../components/reusable/Loading';
import Page from '../components/reusable/Page';
import Form from '../components/reusable/Form';
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

    const navigate = useNavigate();
    const { id } = useParams();
    const baseRoute = '/purchase/'
    const updateRoute = `${baseRoute}${id}/`;

    const purchaseID = `OHMS-${id}-PUR`;
    const heading = `Edit Purchase ${purchaseID}`;
    const text = `Please use this page to edit any information relating to purchase order ${purchaseID}, including adding materials purchased. The cost field when adding a material should be the total amount spent on the selected material alone. The unit cost, inventory level, and total fields will update automatically.`;

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

    const formsets = [
        {entity: 'Material', route: '/purchase/material/', fields: materialFields}
    ]

    return (
        <Page heading={heading} text={text}>
            {loading ? <Loading /> : (
                <Form method='patch' route={updateRoute} baseRoute={baseRoute} initialData={data} initialFiles={{images: data['images']}} buttonText='Save' buttonStyle='success' onSuccess={handleSuccess} fields={fields} formsets={formsets} id={id} fetchData={fetchData} />
            )}
        </Page>
    )
}

export default EditPurchase;
