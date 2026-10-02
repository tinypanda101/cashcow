// const toDate = (value) => (value ? new Date(value) : null);


// Prebuild all the tables here for easy configuration later
export const TABLES = {
    atms: {
        label: 'ATMS',
        endpoint: '/atm',
        columns: [
            { field: 'id', headerName: "ID", width: 80},
            { field: 'serial_number', headerName: "Serial", width: 80},
            { field: 'model', headerName: "Model", width: 80},
            { field: 'status', headerName: "Status", width: 80},
            { field: 'cash_level', headerName: "Cash %", width: 80},
            { field: 'branch_id', headerName: 'Branch ID', width: 80},
        ],
    },
    branches: {
        label: 'Branches',
        endpoint: '/branch',
        columns: [
            { field: 'id', headerName: "ID", width: 80},
            { field: 'name', headerName: "Name", width: 80},
            { field: 'location_region', headerName: "Region", width: 80},
            { field: 'capacity', headerName: "Capacity", width: 80},
            { field: 'supervisor_id', headerName: "Supervisor ID", width: 80},
        ],
    },
    diagnostic_reports: {
        label: 'Diagnostic Reports',
        endpoint: '/diagnostic-reports',
        columns: [
            { field: 'id', headerName: "ID", width: 80},
            { field: 'service_call_id', headerName: "Service Call ID", width: 80},
            { field: 'file_url', headerName: "File Link", width: 80},
            { field: 'notes', headerName: "Notes", width: 80},
            { field: 'timestamp', headerName: "Timestamp", width: 80},
        ],
    },
    service_calls: {
        label: 'Service Calls',
        endpoint: '/service_calls',
        columns: [
            { field: 'id', headerName: "ID", width: 80},
            { field: 'title', headerName: "Title", width: 80},
            { field: 'priority', headerName: "Priority Level", width: 80},
            { field: 'status', headerName: "Status Level", width: 80},
            { field: 'atm_id', headerName: "ATM ID", width: 80},
            { field: 'technician_id', headerName: "Technician ID", width:80},
        ],
    },
    technicians: {
        label: 'Technicians',
        endpoint: '/technician',
        columns: [
            { field: 'id', headerName: "ID", width: 80},
            { field: 'name', headerName: "Name", width: 80},
            { field: 'branch_id', headerName: "Branch ID", width: 80},
       ],
    },
 

};

export const DEFAULT_TABLE = 'atms';