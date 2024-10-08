import { useState, useEffect, useCallback } from 'react';
import CreateModal from './modal/CreateModal';
import UpdateModal from './modal/UpdateModal';
import DeleteModal from './modal/DeleteModal';
import PropTypes from 'prop-types';
import Loading from './Loading';
import api from '../../api';
import $ from 'jquery';

import 'datatables.net-bs4';
import 'datatables.net-bs4/css/dataTables.bootstrap4.min.css'

function Table({ name, fields, formsets, extraFields, route, updateType, relatedData }) {
    const [loading, setLoading] = useState(false);
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

    const getRelatedData = (field, itemId) => {
        const related = relatedData.find(rel => rel.name === field.name);
        if (related) {
            const match = related.data.find(relItem => relItem.id === itemId);
            if (field.name === 'supplier_address') {
                return match && match.representation ? match.representation : 'N/A'; // Use the correct key for the address data
            } else if (field.name === 'service') {
                return match ? match.name : 'N/A';
            } else if (field.name === 'supplier') {
                return match ? match.name : 'N/A';
            } else if (field.name === 'customer') {
                return match ? `${match.first_name} ${match.last_name}` : 'N/A';
            }
        } else {
            console.warn(`Related data for field: ${field.name} not found.`);
        }
        return 'N/A';
    };


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
                                            field.type === 'file' || field.name === 'notes' || field.name === 'description' ? (
                                                <></>
                                            ) : (
                                                <th key={`${field.name}-${index}-footer`} className='text-center'>{field.label}</th>
                                            )
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
                                            field.type === 'file' || field.name === 'notes' || field.name === 'description' ? (
                                                <></>
                                            ) : (
                                                <th key={`${field.name}-${index}-footer`} className='text-center'>{field.label}</th>
                                            )
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
                                                    field.type === 'file' || field.name === 'notes' || field.name === 'description' ? (
                                                        null  // Skip rendering for notes and description
                                                    ) : (
                                                        <td key={`${field.name}-${index}-${item.id}`}>
                                                            {field.name === 'customer' || field.name === 'service' || field.name === 'supplier' || field.name === 'supplier_address' ? (
                                                                getRelatedData(field, item[field.name])
                                                            ) : field.name === 'callout' ? (
                                                                <span style={{ color: item[field.name] === '50.0' ? 'green' : 'red' }}>
                                                                    {item[field.name] === '50.0' ? 'Standard' : 'Emergency'}
                                                                </span>
                                                            ) : field.type === 'checkbox' ? (
                                                                <span style={{ color: item[field.name] ? 'green' : 'red' }}>
                                                                    {item[field.name] ? 'True' : 'False'}
                                                                </span>
                                                            ) : (
                                                                item[field.name] || 'N/A'
                                                            )}
                                                        </td>
                                                    )
                                                ))}
                                                {Array.isArray(extraFields) && extraFields.length > 0 && (
                                                    extraFields.map((field, index) => (
                                                        <td key={`${field.name}-${index}${item.pk}-extra`}>{item[field.name]}</td>
                                                    ))
                                                )}
                                                {updateType === 'page' ? (
                                                    <td key={`edit-${item.id}`}><a href={`${route}${item.id}`} className='btn btn-md btn-primary action-btn'>Edit</a></td>
                                                ) : (
                                                    <td key={`edit-${item.id}`}><UpdateModal name={name} fields={fields} route={route} id={item.id} fetchData={fetchData} formsets={formsets} /></td>
                                                )}
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

    relatedData: PropTypes.arrayOf(
        PropTypes.shape({
            name: PropTypes.string.isRequired,
            data: PropTypes.any.isRequired,
        })
    ),
    updateType: PropTypes.string,
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
