import { Tab, Nav, Form, Button, Spinner, Alert, Row, Col, InputGroup } from 'react-bootstrap';
import { supplierAPI, materialAPI, toolAPI } from '../../api';
import { useState, useEffect } from 'react';
import PropTypes from 'prop-types';

export default function PurchaseForm({ initialData, onSubmit, errors, loading }) {
    const [activeTab, setActiveTab] = useState('basic');
    const [formData, setFormData] = useState({
        supplier: '',
        supplier_address: '',
        date: 0,
        tax: 0,
        ...initialData
    });
    const [materials, setMaterials] = useState(initialData?.materials || []);
    const [tools, setTools] = useState(initialData?.tools || []);
    const [suppliers, setSuppliers] = useState([]);
    const [addresses, setAddresses] = useState([]);
    const [existingMaterials, setExistingMaterials] = useState([]);
    const [newMaterials, setNewMaterials] = useState([]);
    const [existingTools, setExistingTools] = useState([]);
    const [newTools, setNewTools] = useState([]);
    const [files, setFiles] = useState([]);

    const tabs = [
        { key: 'basic', label: 'Basic Info' },
        { key: 'materials', label: `Materials (${materials.length})` },
        { key: 'new-materials', label: `New Materials (${newMaterials.length})` },
        { key: 'tools', label: `Tools (${tools.length})` },
        { key: 'new-tools', label: `New Tools (${newTools.length})` },
        { key: 'summary', label: 'Purchase Summary'}
    ]

    useEffect(() => {
        if (initialData) {
            setFormData(initialData);
            setMaterials(initialData.materials || []);
            setTools(initialData.tools || []);
            setFiles({ uploaded_images: initialData.images || []});
        }
    }, [initialData]);

    useEffect(() => {
        const fetchInitialData = async () => {
            try {
                const [supplierRes, materialRes, toolRes] = await Promise.all([
                    supplierAPI.getSuppliers(),
                    materialAPI.getMaterials(),
                    toolAPI.getTools()
                ]);
                setSuppliers(supplierRes.data);
                setExistingMaterials(materialRes.data);
                setExistingTools(toolRes.data);
                if (initialData?.supplier) {
                    const addressRes = await supplierAPI.getAddresses(initialData.supplier);
                    setAddresses(addressRes.data);
                }
            } catch (error) {
                console.error('Error fetching suppliers:', error);
            }
        };
        fetchInitialData();
    }, [initialData?.supplier]);

    const handleSupplierChange = async (supplierID) => {
        try {
            const response = await supplierAPI.getAddresses(supplierID);
            setAddresses(response.data);
            setFormData(prev => ({
                ...prev,
                supplier: supplierID,
                supplier_address: ''
            }));
        } catch (error) {
            console.error('Error fetching addresses:', error);
        }
    };

    const handleBasicChange = (field, value) => {
        setFormData(prev => ({ ...prev, [field]: value }));
    };

    const handleFileChange = (e) => {
        setFiles([...e.target.files]);
    };

    const handleMaterialChange = (index, field, value) => {
        const updated = materials.map((item, i) =>
            i === index ? { ...item, [field]: value } : item
        );
        setMaterials(updated);
    };

    const handleNewMaterialChange = (index, field, value) => {
        const updated = newMaterials.map((item, i) =>
            i === index ? { ...item, [field]: value } : item
        );
        setNewMaterials(updated);
    };

    const handleToolChange = (index, field, value) => {
        const updated = tools.map((item, i) =>
            i === index ? { ...item, [field]: value } : item
        );
        setTools(updated);
    };

    const handleNewToolChange = (index, field, value) => {
        const updated = newTools.map((item, i) =>
            i === index ? { ...item, [field]: value }: item
        );
        setNewTools(updated);
    };

    const addMaterial = () => setMaterials([ ...materials, { inventory_item: '', quantity: 0, cost: 0 } ]);

    const addNewMaterial = () => setNewMaterials([ ...newMaterials, { name: '', description: '', size: '', quantity: 1, cost: 0 }]);

    const addTool = () => setTools([ ...tools, { inventory_item: '', quantity: 0, cost: 0 } ]);

    const addNewTool = () => setNewTools([ ...newTools, { name: '', desctiption: '', qquantity: 1, cost: 0 }]);

    const removeMaterial = (index) => setMaterials(materials.filter((_, i) => i !== index));

    const removeNewMaterial = (index) => setNewMaterials(newMaterials.filter((_, i) => i !== index));

    const removeTool = (index) => setTools(tools.filter((_, i) => i !== index));

    const removeNewTool = (index) => setNewTools(newTools.filter((_, i) => i !== index));

    const calculateTotal = (items) => items.reduct((sum, item) => sum + (item.cost || 0), 0);
    const materialTotal = calculateTotal([ ...materials, ...newMaterials ]);
    const toolTotal = calculateTotal([ ...tools, ...newTools ]);
    const subtotal = materialTotal + toolTotal;
    const total = subtotal + (formData.tax || 0);

    const handleSubmit = (e) => {
        e.preventDefault();
        onSubmit({
            ...formData,
            materials,
            newMaterials,
            tools,
            newTools,
            uploaded_images: files
        });
    };

    const renderBasicTab = () => (
        <Tab.Pane eventKey='basic'>
            <Row className='g-3'>
                <Col md={6}>
                    <Form.Group controlId='supplier'>
                        <Form.Label>Supplier</Form.Label>
                        <Form.Select required value={formData.supplier}
                            onChange={(e) => handleSupplierChange(e.target.value)}
                            isInvalid={!!errors.supplier}
                        >
                            <option value=''>Select Supplier</option>
                            {suppliers.map(supplier => (
                                <option key={supplier.id} value={supplier.id}>
                                    {supplier.name}
                                </option>
                            ))}
                        </Form.Select>
                        <Form.Control.Feedback type='invalid'>
                            {errors.supplier}
                        </Form.Control.Feedback>
                    </Form.Group>
                </Col>
                <Col md={6}>
                    <Form.Group controlId='supplier_address'>
                        <Form.Label>Supplier Address</Form.Label>
                        <Form.Select required value={formData.supplier_address}
                            onChange={(e) => handleBasicChange('supplier_address', e.target.value)}
                            isInvalid={!!errors.supplier_address}
                            disabled={!formData.supplier}
                        >
                            <option value=''>Select Address</option>
                            {addresses.map(address => (
                                <option key={address.id} value={address.id}>
                                    {`${address.street_address}, ${address.city}, ${address.state} ${address.zip}`}
                                </option>
                            ))}
                        </Form.Select>
                        <Form.Control.Feedback type='invalid'>
                            {errors.supplier_address}
                        </Form.Control.Feedback>
                    </Form.Group>
                </Col>
                <Col md={4}>
                    <Form.Group controlId='date'>
                        <Form.Label>Purchase Date</Form.Label>
                        <Form.Control required type='date' value={formData.date}
                            onChange={(e) => handleBasicChange('date', e.target.value)}
                            isInvalid={!!errors.date}
                        />
                        <Form.Control.Feedback type='invalid'>
                            {errors.date}
                        </Form.Control.Feedback>
                    </Form.Group>
                </Col>
                <Col md={4}>
                    <Form.Group controlId='tax'>
                        <Form.Label>Tax Amount ($)</Form.Label>
                        <InputGroup>
                            <InputGroup.Text>$</InputGroup.Text>
                            <Form.Control type='number' value={formData.tax} min='0' step='0.01'
                                onChange={(e) => handleBasicChange('tax', parseFloat(e.target.value))}
                                isInvalid={!!errors.tax}
                            />
                            <Form.Control.Feedback type='invalid'>
                                {errors.tax}
                            </Form.Control.Feedback>
                        </InputGroup>
                    </Form.Group>
                </Col>
                <Col md={4}>
                    <Form.Group controlId='receipt'>
                        <Form.Label>Receipt Images</Form.Label>
                        <Form.Control type='file' multiple accept='image/*' onChange={handleFileChange} />
                        <Form.Text muted>Upload PNG, JPG, or JPEG files</Form.Text>
                    </Form.Group>
                </Col>
                <Col md={12} className='mt-3'>
                    <div className='d-flex justify-content-end'>
                        <Button variant='primary' onClick={() => setActiveTab('materials')}
                            disabled={!formData.supplier || !formData.supplier_address || !formData.date}
                        >Next</Button>
                    </div>
                </Col>
            </Row>
        </Tab.Pane>
    );

    const renderMaterialsTab = () => (
        <Tab.Pane eventKey='materials'>
            {materials.map((material, index) => (
                <div key={index} className='border p-3 mb-3 rounded'>
                    <Row className='g-3 align-items-center'>
                        <Col md={5}>
                            <Form.Group controlId={`material-${index}`}>
                                <Form.Label>Material</Form.Label>
                                <Form.Select value={material.inventory_item}
                                    onChange={(e) => handleMaterialChange(index, 'inventory_item', e.target.value)}
                                    isInvalid={!!errors[`materials.${index}.inventory_item`]}
                                >
                                    <option value=''>Select Material</option>
                                    {existingMaterials.map(mat => (
                                        <option key={mat.id} value={mat.id}>
                                            {mat.name} ({mat.size})
                                        </option>
                                    ))}
                                </Form.Select>
                            </Form.Group>
                        </Col>
                        <Col md={3}>
                            <Form.Group controlId={`quantity-${index}`}>
                                <Form.Label>Quantity</Form.Label>
                                <Form.Control type='number' min='1' value={material.quantity}
                                    onChange={(e) => handleMaterialChange(index, 'quantity', parseInt(e.target.value))}
                                    isInvalid={!!errors[`materials.${index}.quantity`]}
                                />
                            </Form.Group>
                        </Col>
                        <Col md={3}>
                            <Form.Group controlId={`cost-${index}`}>
                                <Form.Label>Cost</Form.Label>
                                <InputGroup>
                                    <InputGroup.Text>$</InputGroup.Text>
                                    <Form.Control type='number' min='0' step='0.01' value={material.cost}
                                        onChange={(e) => handleMaterialChange(index, 'cost', parseFloat(e.target.value))}
                                        isInvalid={!!errors[`materials.${index}.cost`]}
                                    />
                                </InputGroup>
                            </Form.Group>
                        </Col>
                        <Col md={1} className='d-flex align-items-end'>
                            <Button variant='danger' className='mt-2' onClick={() => removeMaterial(index)}>x</Button>
                        </Col>
                    </Row>
                </div>
            ))}
            <div className='d-flex justify-content-between mt-4'>
                <Button variant='secondary' onClick={() => setActiveTab('basic')}>Back</Button>
                <div>
                    <Button variant='success' onClick={addMaterial} className='me-2'>Add Material</Button>
                    <Button variant='primary' onClick={setActiveTab('new-materials')}>Next</Button>
                </div>
            </div>
        </Tab.Pane>
    );

    const renderNewMaterialsTab = () => (
        <Tab.Pane eventKey='new-materials'>
            {newMaterials.map((material, index) => (
                <div key={index} className='border p-3 mb-3 rounded'>
                    <Row className='g-3'>
                        <Col md={4}>
                            <Form.Group>
                                <Form.Label>Material Name</Form.Label>
                                <Form.Control required value={material.name}
                                    onChange={(e) => handleNewMaterialChange(index, 'name', e.target.value)}
                                    isInvalid={!!errors[`newMaterials.${index}.name`]}
                                />
                            </Form.Group>
                        </Col>
                        <Col md={4}>
                            <Form.Group>
                                <Form.Label>Description</Form.Label>
                                <Form.Control value={material.description}
                                    onChange={(e) => handleNewMaterialChange(index, 'description', e.target.value)}
                                    isInvalid={!!errors[`newMaterials.${index}.description`]}
                                />
                            </Form.Group>
                        </Col>
                        <Col md={4}>
                            <Form.Group>
                                <Form.Label>Size</Form.Label>
                                <Form.Control required value={material.size}
                                    onChange={(e) => handleNewMaterialChange(index, 'size', e.target.value)}
                                    isInvalid={!!errors[`newMaterials.${index}.size`]}
                                />
                            </Form.Group>
                        </Col>
                        <Col md={3}>
                            <Form.Group controlId={`quantity-${index}`}>
                                <Form.Label>Quantity</Form.Label>
                                <Form.Control type='number' min='1' value={material.quantity}
                                    onChange={(e) => handleNewMaterialChange(index, 'quantity', parseInt(e.target.value))}
                                    isInvalid={!!errors[`newMaterials.${index}.quantity`]}
                                />
                            </Form.Group>
                        </Col>
                        <Col md={3}>
                            <Form.Group controlId={`cost-${index}`}>
                                <Form.Label>Cost</Form.Label>
                                <InputGroup>
                                    <InputGroup.Text>$</InputGroup.Text>
                                    <Form.Control type='number' min='0' step='0.01' value={material.cost}
                                        onChange={(e) => handleNewMaterialChange(index, 'cost', parseFloat(e.target.value))}
                                        isInvalid={!!errors[`newMaterials.${index}.cost`]}
                                    />
                                </InputGroup>
                            </Form.Group>
                        </Col>
                        <Col md={1} className='d-flex align-items-end'>
                            <Button variant='danger' className='mt-2' onClick={() => removeNewMaterial(index)}>x</Button>
                        </Col>
                    </Row>
                </div>
            ))}
            <div className='d-flex justify-content-between mt-4'>
                <Button variant='secondary' onClick={() => setActiveTab('materials')}>Back</Button>
                <div>
                    <Button variant='success' onClick={addNewMaterial} className='me-2'>Add New Material</Button>
                    <Button variant='primary' onClick={setActiveTab('tools')}>Next</Button>
                </div>
            </div>
        </Tab.Pane>
    );

    const renderToolsTab = () => (
        <Tab.Pane eventKey='tools'>
            {tools.map((tool, index) => (
                <div key={index} className='border p-3 mb-3 rounded'>
                    <Row className='g-3 align-items-center'>
                        <Col md={5}>
                            <Form.Group controlId={`tool-${index}`}>
                                <Form.Label>Tool</Form.Label>
                                <Form.Select valule={tool.inventory_item}
                                    onChange={(e) => handleToolChange(index, 'inventory_item', e.target.value)}
                                    isInvalid={!!errors[`tools.${index}.inventory_item`]}
                                >
                                    <option value=''>Select Tool</option>
                                    {existingTools.map(t => (
                                        <option key={t.id} value={t.id}>
                                            {t.name}
                                        </option>
                                    ))}
                                </Form.Select>
                            </Form.Group>
                        </Col>
                        <Col md={3}>
                            <Form.Group controlId={`tool-cost-${index}`}>
                                <Form.Label>Cost</Form.Label>
                                <InputGroup>
                                    <InputGroup.Text>$</InputGroup.Text>
                                    <Form.Control type='number' min='0' step='0.01' value={tool.cost}
                                        onChange={(e) => handleToolChange(index, 'cost', parseFloat(e.target.value))}
                                        isInvalid={!!errors[`tools.${index}.cost`]}
                                    />
                                </InputGroup>
                            </Form.Group>
                        </Col>
                        <Col md={1} className='d-flex align-items-end'>
                            <Button variant='danger' onClick={() => removeTool(index)} className='mt-2'>x</Button>
                        </Col>
                    </Row>
                </div>
            ))}
            <div className='d-flex justify-content-between mt-4'>
                <Button variant='secondary' onClick={() => setActiveTab('new-materials')}>Back</Button>
                <div>
                    <Button variant='success' onClick={addTool} className='me-2'>Add Tool</Button>
                    <Button variant='primary' onClick={setActiveTab('new-tools')}>Next</Button>
                </div>
            </div>
        </Tab.Pane>
    );

    const renderNewToolsTab = () => (
        <Tab.Pane eventKey='new-tools'>
            {newTools.map((tool, index) => (
                <div key={index} className='border p-3 mb-3 rounded'>
                    <Row className='g-3'>
                        <Col md={4}>
                            <Form.Group>
                                <Form.Label>Tool Name</Form.Label>
                                <Form.Control required value={tool.name}
                                    onChange={(e) => handleNewToolChange(index, 'name', e.target.value)}
                                    isInvalid={!!errors[`newTools.${index}.name`]}
                                />
                            </Form.Group>
                        </Col>
                        <Col md={4}>
                            <Form.Group>
                                <Form.Label>Description</Form.Label>
                                <Form.Control value={tool.description}
                                    onChange={(e) => handleNewToolChange(index, 'description', e.target.value)}
                                    isInvalid={!!errors[`newTools.${index}.description`]}
                                />
                            </Form.Group>
                        </Col>
                        <Col md={3}>
                            <Form.Group controlId={`quantity-${index}`}>
                                <Form.Label>Quantity</Form.Label>
                                <Form.Control type='number' min='1' value={tool.quantity}
                                    onChange={(e) => handleNewToolChange(index, 'quantity', parseInt(e.target.value))}
                                    isInvalid={!!errors[`newTools.${index}.quantity`]}
                                />
                            </Form.Group>
                        </Col>
                        <Col md={3}>
                            <Form.Group controlId={`cost-${index}`}>
                                <Form.Label>Cost</Form.Label>
                                <InputGroup>
                                    <InputGroup.Text>$</InputGroup.Text>
                                    <Form.Control type='number' min='0' step='0.01' value={tool.cost}
                                        onChange={(e) => handleNewToolChange(index, 'cost', parseFloat(e.target.value))}
                                        isInvalid={!!errors[`newTools.${index}.cost`]}
                                    />
                                </InputGroup>
                            </Form.Group>
                        </Col>
                        <Col md={1} className='d-flex align-items-end'>
                            <Button variant='danger' className='mt-2' onClick={() => removeNewTool(index)}>x</Button>
                        </Col>
                    </Row>
                </div>
            ))}
            <div className='d-flex justify-content-between mt-4'>
                <Button variant='secondary' onClick={() => setActiveTab('tools')}>Back</Button>
                <div>
                    <Button variant='success' onClick={addNewTool} className='me-2'>Add New Tool</Button>
                    <Button variant='primary' onClick={setActiveTab('summary')}>Next</Button>
                </div>
            </div>
        </Tab.Pane>
    );

    const renderSummaryTab = () => (
        <Tab.Pane eventKey='summary'>
            <div className='mt-4 p-3 bg-light rounded'>
                <Row className='g-3'>
                    <Col md={3}>
                        <Form.Group>
                            <Form.Label>Material Total</Form.Label>
                            <InputGroup>
                                <InputGroup.Text>$</InputGroup.Text>
                                <Form.Control type='text' value={materialTotal.toFixed(2)} readonly />
                            </InputGroup>
                        </Form.Group>
                    </Col>
                    <Col md={3}>
                        <Form.Group>
                            <Form.Label>Tool Total</Form.Label>
                            <InputGroup>
                                <InputGroup.Text>$</InputGroup.Text>
                                <Form.Control type='text' value={toolTotal.toFixed(2)} readonly />
                            </InputGroup>
                        </Form.Group>
                    </Col>
                    <Col md={3}>
                        <Form.Group>
                            <Form.Label>Subtotal</Form.Label>
                            <InputGroup>
                                <InputGroup.Text>$</InputGroup.Text>
                                <Form.Control type='text' value={subtotal.toFixed(2)} readonly />
                            </InputGroup>
                        </Form.Group>
                    </Col>
                    <Col md={3}>
                        <Form.Group>
                            <Form.Label>Total</Form.Label>
                            <InputGroup>
                                <InputGroup.Text>$</InputGroup.Text>
                                <Form.Control className='fw-bold' type='text' value={total.toFixed(2)} readonly />
                            </InputGroup>
                        </Form.Group>
                    </Col>
                </Row>
            </div>
            <div className='d-flex justify-content-between mt-4'>
                <Button variant='secondary' onClick={() => setActiveTab('new-tools')}>Back</Button>
                <div>
                    <Button variant='primary' type='submit' disabled={loading}>
                        {loading ? (
                            <Spinner animation='border' size='sm' />
                        ) : initialData ? 'Update Purchase' : 'Create Purchase'}
                    </Button>
                </div>
            </div>
        </Tab.Pane>
    );

    return (
        <Form onSubmit={handleSubmit}>
            <Tab.Container activeKey={activeTab}>
                <Nav variant='tabs' className='mb-3'>
                    {tabs.map(tab => (
                        <Nav.Item key={tab.key}>
                            <Nav.Link eventKey={tab.key}>{tab.label}</Nav.Link>
                        </Nav.Item>
                    ))}
                </Nav>
                <Tab.Content>
                    {renderBasicTab()}
                    {renderMaterialsTab()}
                    {renderNewMaterialsTab()}
                    {renderToolsTab()}
                    {renderNewToolsTab()}
                    {renderSummaryTab()}
                </Tab.Content>
            </Tab.Container>
            {Object.keys(errors).length > 0 && (
                <Alert variant='danger' className='mt-3'>
                    Please fix the errors in the form:
                    <ul className='mb-0'>
                        {Object.entries(errors).map(([field, error]) => (
                            <li key={field}>{error}</li>
                        ))}
                    </ul>
                </Alert>
            )}
        </Form>
    );
};

PurchaseForm.propTypes = {
    onSubmit: PropTypes.func.isRequired,
    loading: PropTypes.bool.isRequired,
    errors: PropTypes.object.isRequired,
    initialData: PropTypes.shape({
        id: PropTypes.number,
        supplier: PropTypes.number,
        supplier_address: PropTypes.number,
        date: PropTypes.string,
        tax: PropTypes.number,
        materials: PropTypes.arrayOf(PropTypes.shape({
            inventory_item: PropTypes.number,
            quantity: PropTypes.number,
            cost: PropTypes.number
        })),
        tools: PropTypes.arrayOf(PropTypes.shape({
            inventory_item: PropTypes.number,
            quantity: PropTypes.number,
            cost: PropTypes.number
        })),
        images: PropTypes.array
    })
};
