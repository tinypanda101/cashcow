/*
    MaintenanceFlagsDataGrid lists Branches with >30% of equipment flagged for maintenance.
*/

import { useEffect, useState } from 'react';
import { DataGrid } from '@mui/x-data-grid';
import { Alert, Box, CircularProgress } from '@mui/material';
import apiClient from '../../api/client.js';


const pct = (v) => (v == null ? '—' : `${Number(v).toFixed(1)}%`);

const columns = [
  { field: 'branch_name', headerName: 'Branch', width: 200 },
  { field: 'branch_id', headerName: 'Branch ID', width: 120, type: 'number' },
  { field: 'total_atms', headerName: 'Total ATMs', width: 130, type: 'number' },
  { field: 'maintenance_count', headerName: 'In Maintenance', width: 150, type: 'number' },
  {
    field: 'maintenance_percentage',
    headerName: 'Maintenance %',
    width: 150,
    type: 'number',
    valueFormatter: (value) => pct(value),
  },
];

function MaintenanceFlagsDataGrid() {
  const [rows, setRows] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let isMounted = true;

    async function fetchFlags() {
      try {
        const response = await apiClient.get('/branch/maintenance');
        if (isMounted) setRows(response.data);
      } catch (err) {
        console.error('Maintenance flags fetch failed:', err);
        if (isMounted) setError('Could not load maintenance flags.');
      } finally {
        if (isMounted) setLoading(false);
      }
    }

    fetchFlags();

    return () => {
      isMounted = false;
    };
  }, []);

  if (loading) return <CircularProgress />;
  if (error) return <Alert severity="error">{error}</Alert>;

  return (
    <Box sx={{ height: 400, width: '100%' }}>
      <DataGrid
        rows={rows}
        columns={columns}
        getRowId={(row) => row.branch_id}
        
      />
    </Box>
  );
}

export default MaintenanceFlagsDataGrid;