import { useState } from 'react';
import {
  Box, Card, CardContent, Typography, TextField,
  Select, MenuItem, InputLabel, FormControl, Button, Alert,
} from '@mui/material';
import apiClient from '../../api/client.js';

const STATUSES = ['Pending', 'In-Progress', 'Completed', 'Failed'];

function ServiceStatusChange() {
  const [serviceId, setServiceId] = useState('');
  const [status, setStatus] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [feedback, setFeedback] = useState(null); // { severity, message }

  async function handleSubmit() {
    if (!serviceId.trim() || !status) {
      setFeedback({ severity: 'warning', message: 'Enter a Service ID and select a status.' });
      return;
    }
    setSubmitting(true);
    setFeedback(null);
    try {
      await apiClient.patch(
        `/service_calls/${serviceId.trim()}/status`,
        { status }
      );
      setFeedback({ severity: 'success', message: `Service ${serviceId.trim()} set to ${status}.` });
    } catch (err) {
      if (err.response?.status === 404) {
        setFeedback({ severity: 'error', message: 'Service not found.' });
      } else {
        console.error('Status update failed:', err);
        setFeedback({ severity: 'error', message: 'Could not update service status.' });
      }
    } finally {
      setSubmitting(false);
    }
  }

  return (
   <Box
      sx={{
        p: 3,
        border: '1px solid',
        borderColor: 'divider',
        borderRadius: 1,
        maxWidth: 560,
      }}
    >
        <Typography variant="h6" align="center" gutterBottom>
          Change Service Status
        </Typography>
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
          <TextField
            label="Service ID"
            value={serviceId}
            onChange={(e) => setServiceId(e.target.value)}
            size="small"
          />
          <FormControl size="small">
            <InputLabel id="status-label">New Status</InputLabel>
            <Select
              labelId="status-label"
              label="New Status"
              value={status}
              onChange={(e) => setStatus(e.target.value)}
            >
              {STATUSES.map((s) => (
                <MenuItem key={s} value={s}>{s}</MenuItem>
              ))}
            </Select>
          </FormControl>
          <Button
            variant="contained"
            onClick={handleSubmit}
            disabled={submitting}
          >
            {submitting ? 'Updating…' : 'Update Status'}
          </Button>
          {feedback && <Alert severity={feedback.severity}>{feedback.message}</Alert>}
        </Box>
      </Box>
  );
}

export default ServiceStatusChange;