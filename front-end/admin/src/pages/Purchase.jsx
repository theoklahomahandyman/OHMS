import Table from '../components/reusable/Table';
import Page from '../components/reusable/Page';
import { useState, useEffect } from 'react';
import toast from 'react-toastify';
import api from '../api';

function Purchase() {
    const [suppliers, setSuppliers] = useState([]);
    const [addresses, setAddresses] = useState([]);
    const [materials, setMaterials] = useState([]);
    const [supplier, setSupplier] = useState(null);

    // Fetch suppliers on component mount
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

    // Fetch materials on component mount
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

    // Fetch addresses when supplier is selected
    useEffect(() => {
        if (supplier) {
            async function fetchAddresses() {
                try {
                    const response = await api.get(`/supplier/addresses/${supplier}`);
                    setAddresses(response.data);
                } catch {
                    toast.error('No Addresses Found!');
                }
            }
            fetchAddresses();
        }
    }, [supplier]);

    // Handle supplier selection change
    const handleSupplierChange = (event) => {
        setSupplier(event.target.value)
    }

    const fields = [
        {name: 'supplier', label: 'Supplier', required: true, elementType: 'select', data: suppliers.map(supplier => ({ value: supplier.id, label: supplier.name })), onChange: handleSupplierChange},
        {name: 'supplier_address', label: 'Supplier Address', required: true, elementType: 'select', data: {/* data for supplier addresses */}},
        {name: 'tax', label: 'Tax Amount', required: false, elementType: 'input', type: 'number', minValue: 0.00},
        {name: 'total', label: 'Total Amount', required: false, elementType: 'input', type: 'number', minValue: 0.00},
        {name: 'date', label: 'Date', required: true, elementType: 'input', type: 'date'},
        {name: 'reciept', label: 'Reciept', required: true, elementType: 'input', type: 'file', multiple: false, accept: 'image/*'},
    ];

    const materialFields = [
        {name: 'material', label: 'Material', required: true, elementType: 'select', data: {/* data for materials */}},
        {name: 'quantity', label: 'Quantity', type: 'number', required: true, elementType: 'input'},
        {name: 'cost', label: 'Cost', type: 'number', required: true, elementType: 'input'},
    ];

    const formsets = [
        {entity: 'Material', route: '/purchase/material/', fields: materialFields}
    ]

    return (
        <Page>
            <h1 className="h3 mb-2 text-gray-800 text-center">Purchases</h1>
            <p className="mb-4 text-center">
                Purchases are acquisitions of materials from suppliers. They are used to increase inventory levels for materials.
            </p>
            <Table fields={fields} name='Purchase' route='/purchase/' formsets={formsets} />
        </Page>
    )
}

export default Purchase;
