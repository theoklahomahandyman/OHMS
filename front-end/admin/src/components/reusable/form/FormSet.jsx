import { useState, useEffect, useCallback } from 'react';
import { createRoot } from 'react-dom/client';
import makeRequest from '../../../api';
import PropTypes from 'prop-types';
import Loading from '../Loading';
import SubForm from './SubForm';

function FormSet({ entity, fields, route, fetchRelatedData, id, newEntity }) {
    const [loading, setLoading] = useState(false);
    const [data, setData] = useState([]);

    route = `${route}${id}/`;

    const formatDate = (isoString) => {
        const date = new Date(isoString);
        return date.toISOString().slice(0, 16);
    };

    const fetchData = useCallback(async () => {
        if (!newEntity) {
            setLoading(true);
            try {
                const response = await makeRequest('get', route);
                const responseData = response.data || [];
                if (Array.isArray(responseData) && response.data.length > 0) {
                    responseData.forEach(item => {
                        if (item.start) {
                            item.start = formatDate(item.start);
                        }
                        if (item.end) {
                            item.end = formatDate(item.end);
                        }
                    })
                }
                setData(responseData)
            } catch {
                setData([]);
            } finally {
                setLoading(false);
            }
        }
    }, [route, newEntity]);

    useEffect(() => {
        fetchData();
    }, [fetchData]);

    const addSubForm = () => {
        const list = document.getElementById(`${entity}-list`);
        const newFormWrapper = document.createElement('div');
        list.appendChild(newFormWrapper);
        const root = createRoot(newFormWrapper);
        root.render(<SubForm fields={fields} route={route} isNew={true} fetchData={fetchData} fetchRelatedData={fetchRelatedData} name={entity} />);
    }

    return (
        <div id={`${entity}-formset`} className='mb-4'>
            <div id={`${entity}-list`}>
                {newEntity ? <></> : (
                    <>
                        <h3 className="text-center m-2">{entity}s</h3>
                        {loading ? <Loading /> : (
                            Array.isArray(data) && data.length > 0 ? (
                                data.map((item, index) => (
                                    <SubForm key={`${index}-${item.pk}-form`} fields={fields} route={route} isNew={false} fetchData={fetchData} fetchRelatedData={fetchRelatedData} initialData={item} id={item.id} name={entity} />
                                ))
                            ) : (
                                <p className="text-center">No {entity}s Yet</p>
                            )
                        )}
                    </>
                )}
            </div>
            <div className='d-flex justify-content-center mt-3'>
                <button className='btn btn-success text-center' onClick={addSubForm} type='button'>{newEntity ? 'Add New' : 'Add'}</button>
            </div>
        </div>
    )
}

FormSet.propTypes = {
    id: PropTypes.any.isRequired,
    entity: PropTypes.string.isRequired,
    route: PropTypes.string.isRequired,
    newEntity: PropTypes.bool.isRequired,
    fetchRelatedData: PropTypes.func,
    fields: PropTypes.arrayOf(
        PropTypes.shape({
            name: PropTypes.string.isRequired,
            label: PropTypes.string.isRequired,
            type: PropTypes.string,
            required: PropTypes.bool.isRequired,
            elementType: PropTypes.string.isRequired,
            maxLength: PropTypes.number,
            minLength: PropTypes.number,
            data: PropTypes.arrayOf(PropTypes.shape({
                value: PropTypes.oneOfType([PropTypes.string, PropTypes.number]).isRequired,
                label: PropTypes.string.isRequired
            })),
            customChange: PropTypes.func,
            disabled: PropTypes.bool,
        })
    ).isRequired,
}

export default FormSet;
