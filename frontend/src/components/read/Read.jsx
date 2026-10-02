import apiClient from '../../api/client.js';
import {TABLES, DEFAULT_TABLE} from './Tables.jsx';
import {useEffect, useState} from 'react';
import {Box, Typography, FormControl, InputLabel, Select, MenuItem, Alert, TextField} from '@mui/material';
import {DataGrid} from '@mui/x-data-grid';


function errorMessage(err,endpoint) {
    const status = err.response?.status;
    const detail = err.repsonse?.data?.detail;
    if (status === 403) return "Your role doesn't have access to this table.";
    if (status === 404 || status === 405) return "No list endpoint at ${endpoint}. Check the path in Tables.jsx";
    if (typeof detail === 'string') return detail;
    return 'Could not load this table.';
}

function TableBuilding() {
    const [tableKey, setTableKey] = useState(DEFAULT_TABLE);
    const [rows, setRows] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error,  setError] = useState(null);

    const table = TABLES[tableKey];

    useEffect(() => {
        const controller = new AbortController();
        setLoading(true);
        setError(null);
        setRows([]);

        apiClient
         .get(table.endpoint, { signal : controller.signal})
         .then((res) => {
            const data = Array.isArray(res.data) ? res.data : res.data?.items ?? [];
            setRows(data);
         })
         .catch((err) => {
            if (err.code == 'ERR_CANCELED') return;
            console.error('Failed to load %{table.endpoint}:', err);
            setErrir(errorMessage(err, table.endpoint));
         })
         .finally(() => {
            if (!controller.signal.aborted) setLoading(false);
         });

         return () => controller.abort();

    }, [table.endpoint]);

    
    return (
        <Box sx={{ height: 400, width: '100%' }}>
            <TextField
                select
                size="small"
                label="Table"
                value={tableKey}
                onChange={(e) => setTableKey(e.target.value)}
                sx = {{minWidth: 220, mb: 2}}
                >

                    {Object.entries(TABLES).map(([key, t]) => (
                        <MenuItem key = {key} value = {key}>{t.label}</MenuItem>
                    ))}
            </TextField>
            
            {error && <Alert severity = "error" sx = {{ mb:2}}>{error}</Alert>}

            <Box sx = {{height:600}}>
                <DataGrid
                key= {tableKey}
                rows= {rows}
                columns= {table.columns}
                loading = {loading}
                showToolbar
                />
            </Box>
        </Box>
    )


}

export default TableBuilding;