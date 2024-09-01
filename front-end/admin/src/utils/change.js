export const formatPhone = (digits) => {
    const parts = digits.match(/^(\d)(\d{3})(\d{3})(\d{4})$/);
    if (!parts) return digits;
    return `${parts[1]} (${parts[2]}) ${parts[3]}-${parts[4]}`;
}

export const handleChange = (event, setData) => {
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
