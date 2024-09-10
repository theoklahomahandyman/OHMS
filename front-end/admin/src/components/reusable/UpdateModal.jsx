import { useState, useEffect } from 'react';
import { toast } from 'react-toastify';
import PropTypes from 'prop-types';
import Loading from './Loading';
import api from '../../api';
import Modal from './Modal';
import Form from './Form';

function UpdateModal({ name, fields, formsets, route, id, fetchData }) {
    const [loading, setLoading] = useState(false);
    const [visible, setVisible] = useState(false);
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
    }

    return (
        <>
            <div className="component">
                <button onClick={() => setVisible(true)} className='btn btn-md btn-primary action-btn'>Edit</button>
            </div>
            <Modal visible={visible} onClose={() => setVisible(false)} title={name}>
                {loading ? <Loading /> : (
                    <>
                        <Form method='patch' route={updateRoute} initialData={data} buttonText='Save' buttonStyle='success' onSuccess={handleSuccess} fields={fields} formsets={formsets} id={id} />
                    </>
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

export default UpdateModal;
