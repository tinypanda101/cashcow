/*
    SupervisorDataGrid lists technicians reporting to a Regional Operations Supervisor
    who currently have active (Pending or In-Progress) service calls.
*/

import { useEffect, useState } from 'react';
import { DataGrid } from '@mui/x-data-grid';
import { Alert, Box, Chip, Stack, TextField } from '@mui/material';
import apiClient from '../../api/client.js';

// change this if your router prefix is different
const SUPERVISOR_ENDPOINT = '/branch/supervisor';

//defines our DataGrid columns and maps them to TechnicianActiveCalls
const columns = [
  { field: 'technician_id', headerName: 'Technician ID', width: 130, type: 'number' },
  { field: 'technician_name', headerName: 'Technician Name', width: 220 },
  { field: 'active_mission_count', headerName: 'Active Calls', width: 130, type: 'number' },
];

function SupervisorDataGrid() {
  const [supervisorId, setSupervisorId] = useState('');
  const [rows, setRows] = useState([]);
  const [technicianCount, setTechnicianCount] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    //supervisor_id is a required query param, so skip the call (and avoid a 422) when it's empty
    if (supervisorId === '') {
      setRows([]);
      setTechnicianCount(null);
      setError(null);
      setLoading(false);
      return;
    }

    let isMounted = true;

    //pulls the supervisor's technicians from the backend
    async function fetchSupervisorTechnicians() {
      setLoading(true);
      setError(null);
      try {
        const response = await apiClient.get(SUPERVISOR_ENDPOINT, {
          params: { supervisor_id: Number(supervisorId) },
        });
        if (isMounted) {
          setRows(response.data.technician);
          setTechnicianCount(response.data.technician_count);
        }
      } catch (err) {
        console.error('Supervisor fetch failed:', err);
        if (isMounted) {
          setError('Could not load technicians for this supervisor.');
          setRows([]);
          setTechnicianCount(null);
        }
      } finally {
        if (isMounted) setLoading(false);
      }
    }

    fetchSupervisorTechnicians();

    return () => {
      isMounted = false;
    };
  }, [supervisorId]);

  //only allow whole numbers in the input
  const handleChange = (event) => {
    const value = event.target.value;
    if (/^\d*$/.test(value)) setSupervisorId(value);
  };

  return (
    <Box sx={{ width: '100%' }}>
      <Stack direction="row" spacing={2} alignItems="center" sx={{ mb: 2 }}>
        <TextField
          label="Supervisor ID"
          value={supervisorId}
          onChange={handleChange}
          inputMode="numeric"
          size="small"
          sx={{ minWidth: 200 }}
        />
        {technicianCount !== null && (
          <Chip
            label={`${technicianCount} technician${technicianCount === 1 ? '' : 's'} with active calls`}
            color={technicianCount > 0 ? 'primary' : 'default'}
          />
        )}
      </Stack>

      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

      <Box sx={{ height: 400, width: '100%' }}>
        <DataGrid
          rows={rows}
          columns={columns}
          loading={loading}
          getRowId={(row) => row.technician_id}
        />
      </Box>
    </Box>
  );
}

export default SupervisorDataGrid;