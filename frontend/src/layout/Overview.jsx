import { Container, Typography, Box } from "@mui/material";
import LowCashDataGrid from '../components/questions/LowCashDataGrid.jsx'
import DiscrepancyDataGrid from '../components/questions/DiscrepancyDataGrid.jsx'
import ReliabilityDataGrid from '../components/questions/ReliabilityDataGrid.jsx'
import MaintenanceFlagsDataGrid from "../components/questions/MaintenanceFlagsDataGrid.jsx";
import SupervisorDataGrid from "../components/questions/SupervisorDataGrid.jsx"

function Overview() {
    return (
        <Container maxWidth = 'lg' sx={{mt:4}}>
        <Typography variant='h5' component='h2' gutterBottom color = 'secondary'>
          Low Cash Active ATMs
        </Typography>
        <Box sx ={{mb : 15}}>
          <LowCashDataGrid/>
        </Box>
        <Typography variant='h5' component='h2' gutterBottom color = 'secondary'>
          Discrepancies
        </Typography>
        <Box sx ={{mb : 15}}>
          <DiscrepancyDataGrid/>
        </Box>
        <Typography variant='h5' component='h2' gutterBottom color = 'secondary'>
          Reliability Metrics
        </Typography>
        <Box sx ={{mb : 15}}>
          <ReliabilityDataGrid/>
        </Box>
        <Typography variant='h5' component='h2' gutterBottom color = 'secondary'>
          Maintenance Flags
        </Typography>
        <Box sx={{mb: 15}}>
          <MaintenanceFlagsDataGrid />
        </Box>
        <Typography variant='h5' component='h2' gutterBottom color = 'secondary'>
          Reporting Lines
        </Typography>
        <Box sx ={{mb : 15}}>
          <SupervisorDataGrid/>
        </Box>

      </Container>

    )
}

export default Overview;