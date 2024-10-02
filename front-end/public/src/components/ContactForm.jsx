import { useState, useEffect } from 'react';
import { toast } from 'react-toastify';
import Loading from './Loading';
import api from '../api';

function ContactForm() {
    const [loading, setLoading] = useState(false);
    const [errors, setErrors] = useState({ first_name: '', last_name: '', email: '', phone: '', description: '' });
    const [files, setFiles] = useState({ uploaded_images: [] });
    const [data, setData] = useState({ first_name: '', last_name: '', email: '', phone: '', description: '' });

    const [confirmEmail, setConfirmEmail] = useState('');

    useEffect(() => {
        const checkEmail = () => {
            if (data['email'] !== confirmEmail) {
                setErrors((prevData) => ({
                    ...prevData,
                    ['confirm_email']: 'Emails must match!'
                }));
            } else {
                setErrors((prevData) => {
                    const updatedErrors = { ...prevData };
                    delete updatedErrors.confirm_email;
                    return updatedErrors;
                });
            }
        }
        checkEmail();
    }, [data, confirmEmail]);

    const onSuccess = () => {
        setData({ first_name: '', last_name: '', email: '', phone: '', description: '' });
        setFiles({ uploaded_images: [] });
        setErrors({ first_name: '', last_name: '', email: '', phone: '', description: '' });
        setConfirmEmail('');
        toast.success('Your request has been successfully submitted. We will be in touch soon!');
    }

    const handleError = (data) => {
        console.log('error response: ', data)
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
                        console.log(data)
                        formattedErrors[fieldName] = ['Unknown error'];
                    }
                }
            }
        }
        setErrors(formattedErrors);
    }

    const formatPhone = (digits) => {
        // Remove any non-digit characters to simplify the formatting logic
        const cleanDigits = digits.replace(/\D/g, '');
        // Start building the formatted number incrementally
        let formatted = '';
        if (cleanDigits.length > 0) {
            // First digit
            formatted += cleanDigits[0];
        }
        if (cleanDigits.length > 1) {
            // Next three digits inside parentheses
            formatted += ' (' + cleanDigits.slice(1, 4);
        }
        if (cleanDigits.length >= 4) {
            // Close the parentheses
            formatted += ') ';
        }
        if (cleanDigits.length >= 5) {
            // Next three digits after the parentheses
            formatted += cleanDigits.slice(4, 7);
        }
        if (cleanDigits.length >= 7) {
            // Add a dash after the next three digits
            formatted += '-' + cleanDigits.slice(7, 11);
        }
        return formatted;
    };

    const handleChange = (event) => {
        const { name, value } = event.target;
        if (name === 'phone') {
            const digits = value.replace(/\D/g, '');
            const formattedPhoneNumber = formatPhone(digits)
            setData((prevData) => ({
                ...prevData,
                phone: formattedPhoneNumber
            }));
        } else {
            setData((prevData) => ({
                ...prevData,
                [name]: value,
            }));
        }
    };

    const handleFileChange = (event) => {
        const { files } = event.target;
        const filesArray = Array.from(files);
        setFiles({ uploaded_images: filesArray });
    };


    const handleSubmit = async (event) => {
        event.preventDefault();
        setLoading(true);
        const formData = new FormData();
        for (const key in data) {
            if (Object.prototype.hasOwnProperty.call(data, key)) {
                formData.append(key, data[key]);
            }
        }
        if (files.uploaded_images && files.uploaded_images.length > 0) {
            files.uploaded_images.forEach((file) => {
                formData.append('uploaded_images', file);
            });
        }
        try {
            const response = await api.post('/order/public/', formData);
            onSuccess(response.data);
        } catch (error) {
            if (error.response && error.response.data) {
                handleError(error.response.data);
            } else {
                handleError({ non_field_errors: ['An unexpected error occured.']});
            }
        } finally {
            setLoading(false);
        }
    }

    return (
        <div>
            <section className="signup-section" id="contact">
                <div className="container px-4 px-lg-5">
                    <div className="row gx-4 gx-lg-5">
                        <div className="col-md-10 col-lg-8 mx-auto text-center">
                            <i className="far fa-paper-plane fa-2x mb-2 text-white"></i>
                            <h2 className="text-white mb-5">Contact us to get started with your project!</h2>
                            <form className="form" id="contactForm" onSubmit={handleSubmit}>
                                {loading ? <Loading /> : (
                                    <>
                                        <div className="row mb-3">
                                            {/* <!-- First name input --> */}
                                            <div className="form-group col-md-6">
                                                <input type="text" id="first_name" name="first_name" value={data['first_name']} onChange={handleChange} className="form-control" required placeholder="John" minLength="2" maxLength="100" />
                                            </div>
                                            {errors['first_name'] && <div className='alert alert-danger mt-2'>{errors['first_name']}</div>}
                                            {/* <!-- Last name input --> */}
                                            <div className="form-group col-md-6">
                                                <input type="text" id="last_name" name="last_name" value={data['last_name']} onChange={handleChange} className="form-control" required placeholder="Doe" minLength="2" maxLength="100" />
                                            </div>
                                            {errors['last_name'] && <div className='alert alert-danger mt-2'>{errors['last_name']}</div>}
                                        </div>
                                        <div className="row mb-3">
                                            {/* <!-- Email input --> */}
                                            <div className="form-group col-md-6">
                                                <input type="email" id="email" name="email" value={data['email']} onChange={handleChange} className="form-control" required placeholder="johndoe@example.com" minLength="8" maxLength="255" />
                                            </div>
                                            {errors['email'] && <div className='alert alert-danger mt-2'>{errors['email']}</div>}
                                            {/* <!-- Confirm email input --> */}
                                            <div className="form-group col-md-6">
                                                <input type="email" id="confirm_email" name="confirm_email" value={confirmEmail} onChange={() => setConfirmEmail(event.target.value)} className="form-control" required placeholder="johndoe@example.com" minLength="8" maxLength="255" />
                                            </div>
                                            {errors['confirm_email'] && <div className='alert alert-danger mt-2'>{errors['confirm_email']}</div>}
                                        </div>
                                        <div className="row mb-3">
                                            {/* <!-- Phone number input --> */}
                                            <div className="form-group col-md-6">
                                                <input type="text" id="phone" name="phone" value={data['phone']} onChange={handleChange} className="form-control" required placeholder="1 (234) 567-8901" minLength="16" maxLength="17" />
                                            </div>
                                            {errors['phone'] && <div className='alert alert-danger mt-2'>{errors['phone']}</div>}
                                            {/* <!-- Optional pictures input --> */}
                                            <div className="form-group col-md-6">
                                                <input type="file" accept='image/*' id="uploaded_images" name="uploaded_images" onChange={handleFileChange} className="form-control" multiple />
                                            </div>
                                            {errors['uploaded_images'] && <div className='alert alert-danger mt-2'>{errors['uploaded_images']}</div>}
                                        </div>
                                        <div className="row mb-3">
                                            {/* <!-- Description input --> */}
                                            <div className="form-group col-12">
                                                <textarea id="description" name="description" value={data['description']} onChange={handleChange} className="form-control" required placeholder="Please write a description of the project..." minLength="2" maxLength="2000"></textarea>
                                            </div>
                                            {errors['description'] && <div className='alert alert-danger mt-2'>{errors['description']}</div>}
                                        </div>
                                        <div className="row mb-3">
                                            {/* <!-- Submit button --> */}
                                            <button id="submit" className="btn btn-primary" type="submit">Submit</button>
                                        </div>
                                    </>
                                )}
                            </form>
                        </div>
                    </div>
                </div>
            </section>
        </div>
    )
}

export default ContactForm;
