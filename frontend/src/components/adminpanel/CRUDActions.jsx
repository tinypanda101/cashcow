import { TABLES } from './CRUDTables.jsx';
import { useState } from 'react';
import { Alert, Box, Button, Card, CardContent, CardHeader, Container, Grid, MenuItem, TextField, ToggleButton, ToggleButtonGroup } from '@mui/material';
import apiClient from '../../api/client.js';
 
function AdminPanel() {
    const [tableKey, setTableKey] = useState('atms');
    const [action, setAction] = useState('create');
    const [id, setId] = useState('');
    const [values, setValues] = useState({});
    const [message, setMessage] = useState(null);
 
    const table = TABLES[tableKey];
 
    function errorText(err) {
        if (!err.response) return 'Could not reach the backend.';
        const detail = err.response.data?.detail;
        if (typeof detail === 'string') return detail; // e.g. "ATM not found with the ID 5"
        if (Array.isArray(detail)) return detail.map((d) => `${d.loc.at(-1)}: ${d.msg}`).join(', '); // 422
        return `Request failed (${err.response.status}).`;
    }
 
 
    // Picking a new table or action starts with an empty form.
    function clearForm() {
        setId('');
        setValues({});
        setMessage(null);
    }
 
    function handleChange(name, value) {
        setValues((prev) => ({ ...prev, [name]: value }));
    }
 
    // Request body: skip blank fields, convert number fields to numbers.
    function buildBody() {
        const body = {};
        for (const field of table.fields) {
            const value = values[field.name];
            if (value === undefined || value === '') continue;
            body[field.name] = field.type === 'number' ? Number(value) : value;
        }
        return body;
    }
 
    async function handleSubmit(event) {
        event.preventDefault();
        setMessage(null);
 
        if (action !== 'create' && !id) {
            setMessage({ type: 'error', text: 'Enter an ID.' });
            return;
        }
        const recordUrl = `${table.endpoint.replace(/\/$/, '')}/${id}`; // e.g. /atm/5
 
        try {
            if (action === 'create') {
                const missing = table.fields.filter((f) => !f.optional && !values[f.name]);
                if (missing.length > 0) {
                    setMessage({ type: 'error', text: `Fill in: ${missing.map((f) => f.label).join(', ')}` });
                    return;
                }
                const res = await apiClient.post(table.endpoint, buildBody());
                setMessage({ type: 'success', text: `Created record #${res.data.id}.` });
            } else if (action === 'update') {
                const body = buildBody();
                if (Object.keys(body).length === 0) {
                    setMessage({ type: 'error', text: 'Fill in at least one field to change.' });
                    return;
                }
                await apiClient.request({ method: table.updateMethod, url: recordUrl, data: body });
                setMessage({ type: 'success', text: `Updated record #${id}: ${Object.keys(body).join(', ')}.` });
            } else {
                if (!window.confirm(`Delete ${table.label} record #${id}? This can't be undone.`)) return;
                await apiClient.delete(recordUrl);
                setMessage({ type: 'success', text: `Deleted record #${id}.` });
            }
            setId('');
            setValues({});
        } catch (err) {
            setMessage({ type: 'error', text: errorText(err) });
        }
    }
 
    return (
        <Container maxWidth="md" sx={{ py: 3 }}>
            <Card>
                <CardHeader title="Admin Panel" />
                <CardContent>
                    {/* Table dropdown + action buttons */}
                    <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap', mb: 3 }}>
                        <TextField
                            select
                            size="small"
                            label="Table"
                            value={tableKey}
                            onChange={(e) => {
                                setTableKey(e.target.value);
                                clearForm();
                            }}
                            sx={{ minWidth: 200 }}
                        >
                            {Object.entries(TABLES).map(([key, t]) => (
                                <MenuItem key={key} value={key}>
                                    {t.label}
                                </MenuItem>
                            ))}
                        </TextField>
 
                        <ToggleButtonGroup
                            exclusive
                            size="small"
                            value={action}
                            onChange={(_, next) => {
                                if (next) {
                                    setAction(next);
                                    clearForm();
                                }
                            }}
                        >
                            <ToggleButton value="create">Create</ToggleButton>
                            <ToggleButton value="update">Update</ToggleButton>
                            <ToggleButton value="delete" color="error">
                                Delete
                            </ToggleButton>
                        </ToggleButtonGroup>
                    </Box>
 
                    {message && (
                        <Alert severity={message.type} sx={{ mb: 2 }}>
                            {message.text}
                        </Alert>
                    )}
 
                    {/* The form: which inputs show depends on the action */}
                    <Box component="form" noValidate onSubmit={handleSubmit}>
                        <Grid container spacing={2}>
                            {action !== 'create' && (
                                <Grid size={{ xs: 12, sm: 6 }}>
                                    <TextField
                                        fullWidth
                                        size="small"
                                        type="number"
                                        label="ID"
                                        value={id}
                                        onChange={(e) => setId(e.target.value)}
                                    />
                                </Grid>
                            )}
 
                            {action !== 'delete' &&
                                table.fields.map((field) => (
                                    <Grid key={field.name} size={{ xs: 12, sm: 6 }}>
                                        <TextField
                                            fullWidth
                                            size="small"
                                            label={field.label}
                                            type={field.options ? undefined : field.type ?? 'text'}
                                            select={Boolean(field.options)}
                                            value={values[field.name] ?? ''}
                                            onChange={(e) => handleChange(field.name, e.target.value)}
                                            helperText={action === 'update' ? 'Leave blank to keep the current value' : ' '}
                                        >
                                            {field.options && action === 'update' && (
                                                <MenuItem value="">
                                                    <em>No change</em>
                                                </MenuItem>
                                            )}
                                            {field.options?.map((option) => (
                                                <MenuItem key={option} value={option}>
                                                    {option}
                                                </MenuItem>
                                            ))}
                                        </TextField>
                                    </Grid>
                                ))}
                        </Grid>
 
                        <Button
                            type="submit"
                            variant="contained"
                            color={action === 'delete' ? 'error' : 'primary'}
                            sx={{ mt: 2 }}
                        >
                            {action === 'create' ? 'Create Record' : action === 'update' ? 'Save Changes' : 'Delete Record'}
                        </Button>
                    </Box>
                </CardContent>
            </Card>
        </Container>
    );
}
 
export default AdminPanel;
 
