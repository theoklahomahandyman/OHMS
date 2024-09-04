import { useState, useEffect } from 'react';
import { toast } from 'react-toastify';
import PropTypes from 'prop-types';
import Loading from './Loading';
import api from '../../api';
import Modal from './Modal';
import Form from './Form';

function UpdateModal({ name, fields, route, id, fetchData }) {
    const [loading, setLoading] = useState(false);
    const [visible, setVisible] = useState(false);
    const [errors, setErrors] = useState({});
    const [data, setData] = useState({});

    const updateRoute = `${route}${id}/`;

    useEffect(() => {
        const fetchData = async () => {
            setLoading(true);
            try {
                const response = await api.get(updateRoute);
                setData(response.data || {});
            } catch {
                setData({});
            } finally {
                setLoading(false);
            }
        }
        fetchData();
    }, [updateRoute]);

    const handleSuccess = () => {
        fetchData();
        toast.success(`${name} successfully updated!`);
        setVisible(false);
        setData({});
        setErrors({});
    }

    const handleError = (data) => {
        const formattedErrors = {};
        if (typeof data === 'object' && !Array.isArray(data)) {
            for (let fieldName in data) {
                if (Object.prototype.hasOwnProperty.call(data, fieldName)) {
                    const array = data[fieldName];
                    if (Array.isArray(array)) {
                        formattedErrors[fieldName] = array;
                    } else if (typeof array === 'string') {
                        formattedErrors[fieldName] = [array];
                    } else {
                        formattedErrors[fieldName] = ['Unknown error'];
                    }
                }
            }
        }
        setErrors(formattedErrors);
    }


    return (
        <>
            <div className="component">
                <button onClick={() => setVisible(true)} className='btn btn-md btn-primary action-btn'>Edit</button>
            </div>
            <Modal visible={visible} onClose={() => setVisible(false)} title={name}>
                {loading ? <Loading /> : (
                    <Form method='patch' route={updateRoute} data={data} buttonText='Save' buttonStyle='success' onSuccess={handleSuccess} onError={handleError} setErrors={setErrors} fields={fields} setData={setData} errors={errors} />
                )}
            </Modal>
        </>
    )
}

UpdateModal.propTypes = {
    name: PropTypes.string.isRequired,
    route: PropTypes.string.isRequired,
    id: PropTypes.number.isRequired,
    fetchData: PropTypes.func.isRequired,
    fields: PropTypes.arrayOf(
        PropTypes.shape({
            name: PropTypes.string.isRequired,
            label: PropTypes.string.isRequired,
            type: PropTypes.string.isRequired,
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
}

export default UpdateModal;
