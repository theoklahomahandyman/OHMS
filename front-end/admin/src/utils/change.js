export const formatPhone = (digits) => {
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

export const handleChange = (event, setData) => {
    const { name, value, type, checked } = event.target;
    if (name === 'phone') {
        const digits = value.replace(/\D/g, '');
        const formattedPhoneNumber = formatPhone(digits)
        setData((prevData) => ({
            ...prevData,
            phone: formattedPhoneNumber
        }));
    } else if (type === 'checkbox') {
        setData((prevData) => ({
            ...prevData,
            [name]: checked,
        }));
    } else {
        setData((prevData) => ({
            ...prevData,
            [name]: value,
        }));
    }
};

export const handleFileChange = (event, setFiles) => {
    const { name, files } = event.target;
    setFiles(prevFiles => ({
        ...prevFiles,
        [name]: [...(prevFiles[name] || []), ...Array.from(files)]
    }));
};
