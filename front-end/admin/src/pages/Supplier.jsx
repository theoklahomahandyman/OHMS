import LocationsModal from '../components/LocationsModal';
import { useState, useEffect, useCallback } from 'react';
import Page from '../components/reusable/Page';
import CreateModal from '../components/reusable/CreateModal';
import UpdateModal from '../components/reusable/UpdateModal';
import DeleteModal from '../components/reusable/DeleteModal';
import Loading from '../components/reusable/Loading';
import api from '../api';
import $ from 'jquery';

import 'datatables.net-bs4';
import 'datatables.net-bs4/css/dataTables.bootstrap4.min.css'

function Supplier() {
    const [loading, setLoading] = useState(false);
    const [data, setData] = useState([]);

    const route = '/supplier/';

    const fields = [
        {name: 'name', label: 'Supplier Name', type: 'text', required: true, maxLength: 255, minLength: 2},
        {name: 'notes', label: 'Supplier Notes', type: 'text', required: false, maxLength: 500, minLength: 0}
    ];

    const fetchData = useCallback(async () => {
        setLoading(true);
        try {
            const response = await api.get(route);
            setData(response.data || []);
        } catch {
            setData([]);
        } finally {
            setLoading(false);
        }
    }, [route]);

    useEffect(() => {
        fetchData();
    }, [fetchData]);

    useEffect(() => {
        if (Array.isArray(data) && data.length > 0) {
            setTimeout(() => {
                $('#dataTable').DataTable();
            }, 1);
        }
    }, [data]);

    return (
        <Page>
            <h1 className="h3 mb-2 text-gray-800 text-center">Suppliers</h1>
            <p className="mb-4 text-center">
                Suppliers are companies or individuals used to acquire materials for work orders and must be specified in purchases.
            </p>
            <div className="card shadow mb-4">
                <div className="card-header py-3 d-flex justify-content-between align-items-center">
                    <h6 className="m-0 font-weight-bold text-primary">Suppliers</h6>
                    <CreateModal name='Suppliers' fields={fields} route={route} fetchData={fetchData}/>
                </div>
                <div className="card-body">
                    {loading ? <Loading /> : (
                        <div className="table-responsive">
                            <table className="table table-bordered m-4" id="dataTable" width="95%" cellSpacing="0">
                                <thead>
                                    <tr>
                                        {fields.map((field, index) => (
                                            <th key={`${field.name}-${index}-header`} className='text-center'>{field.name.charAt(0).toUpperCase() + field.name.slice(1)}</th>
                                        ))}
                                        <th className='text-center'>Locations</th>
                                        <th className='text-center'>Edit</th>
                                        <th className='text-center'>Delete</th>
                                    </tr>
                                </thead>
                                <tfoot>
                                    <tr className='text-center'>
                                        {fields.map((field, index) => (
                                            <th key={`${field.name}-${index}-footer`}>{field.name.charAt(0).toUpperCase() + field.name.slice(1)}</th>
                                        ))}
                                        <th className="text-center">Locations</th>
                                        <th className='text-center'>Edit</th>
                                        <th className='text-center'>Delete</th>
                                    </tr>
                                </tfoot>
                                <tbody>
                                    {Array.isArray(data) && data.length > 0 ? (
                                        data.map((item) => (
                                            <tr className="text-center" key={`${item.pk}-${item.name}`}>
                                                {fields.map((field, index) => (
                                                    <td key={`${field.name}-${index}-${item.pk}`}>{item[field.name]}</td>
                                                ))}
                                                <td key={`locations-${item.id}`}><LocationsModal id={item.id} /></td>
                                                <td key={`edit-${item.id}`}><UpdateModal name='Supplier' fields={fields} route={route} id={item.id} fetchData={fetchData} /></td>
                                                <td key={`delete-${item.id}`}><DeleteModal name='Supplier' route={route} id={item.id} fetchData={fetchData} /></td>
                                            </tr>
                                        ))
                                    ) : (
                                        <tr className="text-center">
                                            <td className="text-center" colSpan={fields.length + 2}>No Data Yet</td>
                                        </tr>
                                    )}
                                </tbody>
                            </table>
                        </div>
                    )}
                </div>
            </div>
        </Page>
    )
}

export default Supplier;
