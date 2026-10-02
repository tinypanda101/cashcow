import { Container, Typography, Box } from "@mui/material";
import UpdateServiceStatus from "../components/techpanel/UpdateServiceStatus.jsx"



function TechPanel() {
  return (
    <Container maxWidth = 'lg' sx={{mt:4}}>
        <Typography variant='h5' component='h2' gutterBottom color = 'secondary'>
          Upload Service Report
        </Typography>
        <Box sx={{ mb: 4 }}>
         {// <ServiceReportUpload />
         }
        </Box>
        <Typography variant='h5' component='h2' gutterBottom color = 'secondary'>
          Status Change for Service Calls
        </Typography>
        <Box sx={{ mb: 4 }}>
          <UpdateServiceStatus />
        </Box>
    </Container>
    )
}

export default TechPanel;