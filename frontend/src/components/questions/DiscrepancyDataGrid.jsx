import { useEffect, useState } from 'react';
import { DataGrid } from '@mui/x-data-grid';
import { Alert, Box, CircularProgress, MenuItem, TextField } from '@mui/material';
import apiClient from '../../api/client.js';

//defines our DataGrid columns and maps them to our backend API response data
const columns = [
  { field: 'servicecall_id', headerName: 'ID', width: 100 },
  { field: 'title', headerName: 'Title', width: 200 },
  { field: 'atm_branch_id', headerName: 'ATM Branch ID', width: 150 },
  { field: 'technician_branch_id', headerName: 'Technician Branch ID', width: 150 }
];

function DiscrepancyDataGrid() {
    const[ Calls, setCalls] = useState([]);
    const[loading, setLoading] = useState(true);
    const[error, setError] = useState(null);
    const[selectedPriority, setSelectedPriority] = useState('');

    useEffect(() => {
        let isMounted = true;

        //pulls from backend
        async function fetchDiscrepancies() {
            try {
                const response = await apiClient.get('/service_calls/discrepancies', {params: {priority: selectedPriority || undefined}});
                if (isMounted) {
                    setCalls(response.data);
                    
                }
            } catch {
                if (isMounted) setError("Could not load discrepancies");
            } finally {
                if (isMounted) setLoading(false);
            }
        }

        fetchDiscrepancies();

        return () => {
            isMounted = false;
        };
    }, [selectedPriority]);

    if (loading) {
        return <CircularProgress />;
    }

    if (error) {
        return <Alert severity="error">{error}</Alert>;
    }

    //loads datagrid
    return (
        <Box sx={{ height: 400, width: '100%' }}>
            <TextField
                select
                label="Priority"
                value={selectedPriority}
                onChange={(e) => setSelectedPriority(e.target.value)}
                sx={{ mb: 2, minWidth: 200 }}
            >
                <MenuItem value="">All</MenuItem>
                <MenuItem value="Low">Low</MenuItem>
                <MenuItem value="Medium">Medium</MenuItem>
                <MenuItem value="Critical">Critical</MenuItem>
            </TextField>
            <DataGrid
                rows={Calls}
                columns={columns}
                pageSize={5}
                rowsPerPageOptions={[5]}
                getRowId={(row) => row.servicecall_id}
            />
        </Box>
    );
}

export default DiscrepancyDataGrid;
