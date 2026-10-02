export const TABLES = {
    atms: {
        label: 'ATMS',
        endpoint: '/atm',
        updateMethod: 'put',
        fields: [
            {name: 'serial_number', label: 'Serial Number'},
            {name: 'model', label: 'Model'},
            {name: 'status', label: 'Status', options: ['Operational', 'In-Transport', 'Maintenance', 'Offline']},
            {name: 'cash_level', label: 'Cash Level (%)', type: 'number'},
            {name: 'branch_id', label: 'Branch ID', type: 'number'},
        ],
    },
    branches: {
        label: 'Branches',
        endpoint: '/branch',
        updateMethod: 'post',
        fields: [
            {name: 'name', label: 'Name'},
            {name: 'location_region', label: 'Region'},
            {name: 'capacity', label: 'Capacity', type: 'number'},
            {name: 'supervisor_id', label: 'Supervisor ID', type: 'number'},
            {name: 'branch_id', label: 'Branch ID', type: 'number'},
        ],
    },
    diagnostic_reports: {
        label: 'Diagnostic Reports',
        endpoint: '/diagnostic-reports',
        updateMethod: 'post',
        fields: [
            {name: 'service_call_id', label: 'Service Call ID', type: 'number'},
            {name: 'file_url', label: 'File URL'},
            {name: 'notes', label: 'Notes', optional: true },
        ],
    },
    service_calls: {
        label: 'Service Calls',
        endpoint: '/service_calls',
        updateMethod: 'put',
        fields: [
            {name: 'title', label: 'Title'},
            {name: 'priority', label: 'Priority Level', options: ['Low', 'Medium', 'Critical']},
            {name: 'status', label: 'Status', options: ['Pending', 'In-Progress', 'Completed', 'Failed']},
            {name: 'atm_id', label: 'ATM ID', type: 'number'},
            {name: 'technician_id', label: 'Technician ID', type: 'number'},
        ],
    },
    technicians: {
        label: 'Technicians',
        endpoint: '/technician',
        updateMethod: 'put',
        fields: [
            {name: 'name', label: 'Name'},
            {name: 'branch_id', label: 'Branch ID', type: 'number'},
        ],
    },
    users: {
        label: 'Users',
        endpoint: '/users',
        updateMethod: 'put',
        fields: [
            {name: 'username', label: 'Username'},
            {name: 'password', label: 'Password', type: 'password'},
            {name: 'role', label: 'Role', options: ['Operations Admin', 'Field Technician', "Auditor"]},
        ],
    },
};