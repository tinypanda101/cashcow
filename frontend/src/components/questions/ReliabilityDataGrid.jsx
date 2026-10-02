import { useEffect, useState } from 'react';
import { DataGrid } from '@mui/x-data-grid';
import { Alert, Box, CircularProgress, MenuItem, TextField } from '@mui/material';
import apiClient from '../../api/client.js';


const pct = (v) => (v == null ? '—' : `${(v * 100).toFixed(1)}%`);
//defines our DataGrid columns and maps them to our backend API response data
const columns = [
    { field: 'model', headerName: 'Model', width: 200 },
    { field: 'total_calls', headerName: 'Total Calls', width: 150 },
    { field: 'completed_count', headerName: 'Completed', width: 150 },
    { field: 'failed_count', headerName: 'Failed', width: 150 },
    { field: 'ratio', headerName: 'Reliability Ratio', width: 150, type: 'number', valueFormatter: (value) => pct(value) },
];


function ReliabilityDataGrid() {
    const[ models, setModels] = useState([]);
    const[loading, setLoading] = useState(true);
    const[error, setError] = useState(null);

    useEffect(() => {
        let isMounted = true;

        //pulls from backend
        async function fetchReliabilityData() {
            try {
                const response = await apiClient.get('/service_calls/completion_ratio');
                if (isMounted) {
                    setModels(response.data);
                    
                }
            } catch {
                if (isMounted) setError("Could not load reliability data");
            } finally {
                if (isMounted) setLoading(false);
            }
        }

        fetchReliabilityData();

        return () => {
            isMounted = false;
        };
    }, []);

    if (loading) {
        return <CircularProgress />;
    }

    if (error) {
        return <Alert severity="error">{error}</Alert>;
    }

    //loads datagrid
   //loads data grid component if all goes well
    return (
    <Box sx={{ height: 400, width: '100%' }}>
        <DataGrid rows={models} columns={columns} getRowId={(row) => row.model} />
    </Box>

    );
}

export default ReliabilityDataGrid;
