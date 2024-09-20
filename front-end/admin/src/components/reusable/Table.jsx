import { useState, useEffect, useCallback } from 'react';
import CreateModal from './CreateModal';
import UpdateModal from './UpdateModal';
import DeleteModal from './DeleteModal';
import PropTypes from 'prop-types';
import Loading from './Loading';
import api from '../../api';
import $ from 'jquery';

import 'datatables.net-bs4';
import 'datatables.net-bs4/css/dataTables.bootstrap4.min.css'

function Table({ name, fields, formsets, extraFields, route }) {
    const [loading, setLoading] = useState(false);
    const [relatedData, setRelatedData] = useState([]);
    const [data, setData] = useState([]);

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

    const fetchRelatedData = async (id, route) => {
        setLoading(true);
        try {
            const response = await api.get(`${route}/${id}/`);
            return response.data;
        } catch {
            return null;
        } finally {
            setLoading(false);
        }
    }

    useEffect(() => {
        fetchData();
    }, [fetchData]);

    useEffect(() => {
        const loadRelatedData = async (item, field) => {
            if (!field.route) return;
            const id = item[field.name];
            const result = await fetchRelatedData(id, field.route);
            setRelatedData(prev => ({ ...prev, [`${item.pk}-${field.name}`]: result }));
        }
        if (Array.isArray(data) && data.length > 0) {
            data.forEach(item => {
                fields.forEach(field => {
                    if (field.elementType === 'select') {
                        loadRelatedData(item, field);
                    }
                });
            });
            setTimeout(() => {
                $('#dataTable').DataTable();
            }, 1);
        }
    }, [data, fields]);

    return (
        <div>
            <div className="card shadow mb-4">
                <div className="card-header py-3 d-flex justify-content-between align-items-center">
                    <h6 className="m-0 font-weight-bold text-primary">{name}s</h6>
                    <CreateModal name={name} fields={fields} route={route} fetchData={fetchData} />
                </div>
                <div className="card-body">
                    {loading ? <Loading /> : (
                        <div className="table-responsive">
                            <table className="table table-bordered m-4" id="dataTable" width="95%" cellSpacing="0">
                                <thead>
                                    <tr>
                                        {fields.map((field, index) => (
                                            <th key={`${field.name}-${index}-header`} className='text-center'>{field.label}</th>
                                        ))}
                                        {Array.isArray(extraFields) && extraFields.length > 0 ? (
                                            extraFields.map((field, index) => (
                                                <th key={`${field.name}-${index}-extra`} className='text-center'>{field.label}</th>
                                            ))
                                        ) : <></>}
                                        <th className='text-center' key='edit-header'>Edit</th>
                                        <th className='text-center' key='delete-header'>Delete</th>
                                    </tr>
                                </thead>
                                <tfoot>
                                    <tr>
                                        {fields.map((field, index) => (
                                            <th key={`${field.name}-${index}-footer`} className='text-center'>{field.label}</th>
                                        ))}
                                        {Array.isArray(extraFields) && extraFields.length > 0 ? (
                                            extraFields.map((field, index) => (
                                                <th key={`${field.name}-${index}-extra`} className='text-center'>{field.label}</th>
                                            ))
                                        ) : <></>}
                                        <th className='text-center' key='edit-footer'>Edit</th>
                                        <th className='text-center' key='delete-footer'>Delete</th>
                                    </tr>
                                </tfoot>
                                <tbody>
                                    {Array.isArray(data) && data.length > 0 ? (
                                        data.map((item, index) => (
                                            <tr className="text-center" key={`${index}-row`}>
                                                {fields.map((field, index) => (
                                                    <td key={`${field.name}-${index}-${item.pk}-data`}>
                                                        {field.name === 'callout' ? (
                                                            <span style={{ color: item[field.name] === '50.0' ? 'green' : 'red' }}>
                                                                {item[field.name] === '50.0' ? 'Standard' : 'Emergency'}
                                                            </span>
                                                        ) :field.type === 'checkbox' ? (
                                                            <span style={{ color: item[field.name] ? 'green' : 'red' }}>{item[field.name] ? 'True' : 'False'}</span>
                                                        ) : field.type === 'file' && field.accept === 'image/*' ? (
                                                            <img src={`http://localhost:8000${item[field.name]}`} alt={field.label} style={{ width: '50px', height: '50px' }} />
                                                        ) : field.elementType === 'select' && field.route ? (
                                                            relatedData[`${item.pk}-${field.name}`]?.representation || <Loading />
                                                        ) : (
                                                            item[field.name]
                                                        )}
                                                    </td>
                                                ))}
                                                {Array.isArray(extraFields) && extraFields.length > 0 ? (
                                                    extraFields.map((field, index) => (
                                                        <td key={`${field.name}-${index}${item.pk}-extra`}>{item[field.name]}</td>
                                                    ))
                                                ) : <></>}
                                                <td key={`edit-${item.id}`}><UpdateModal name={name} fields={fields} route={route} id={item.id} fetchData={fetchData} formsets={formsets} /></td>
                                                <td key={`delete-${item.id}`}><DeleteModal name={name} route={route} id={item.id} fetchData={fetchData} /></td>
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
        </div>
    )
}

Table.propTypes = {
    name: PropTypes.string.isRequired,
    route: PropTypes.string.isRequired,
    fields: PropTypes.arrayOf(
        PropTypes.shape({
            name: PropTypes.string.isRequired,
            label: PropTypes.string.isRequired,
            type: PropTypes.string,
            required: PropTypes.bool.isRequired,
            elementType: PropTypes.string.isRequired,
            maxLength: PropTypes.number,
            minLength: PropTypes.number,
            accept: PropTypes.string,
            multiple: PropTypes.bool,
            data: PropTypes.arrayOf(PropTypes.shape({
                value: PropTypes.oneOfType([PropTypes.string, PropTypes.number]).isRequired,
                label: PropTypes.string.isRequired
            })),
            customChange: PropTypes.func,
            route: PropTypes.string,
        })
    ).isRequired,

    extraFields: PropTypes.array,
    formsets: PropTypes.arrayOf(
        PropTypes.shape({
            entity: PropTypes.string.isRequired,
            route: PropTypes.string.isRequired,
            fields: PropTypes.arrayOf(
                PropTypes.shape({
                    name: PropTypes.string.isRequired,
                    label: PropTypes.string.isRequired,
                    type: PropTypes.string,
                    required: PropTypes.bool.isRequired,
                    elementType: PropTypes.string.isRequired,
                    maxLength: PropTypes.number,
                    minLength: PropTypes.number,
                    accept: PropTypes.string,
                    multiple: PropTypes.bool,
                    data: PropTypes.arrayOf(PropTypes.shape({
                        value: PropTypes.oneOfType([PropTypes.string, PropTypes.number]).isRequired,
                        label: PropTypes.string.isRequired
                    })),
                })
            ).isRequired,
        })
    ),
}

export default Table;
