import { Container, Typography, Box } from "@mui/material";
import TableReads from "../components/read/Read.jsx";
function ReadPanel() {
    return (
        <Container maxWidth = 'lg' sx={{mt:4}}>
            <Typography variant='h5' component='h2' gutterBottom color = 'secondary'>
                Tables
            </Typography>
            <Box sx ={{mb : 4}}>
                <TableReads/>
            </Box>  

        </Container>
    )
}

export default ReadPanel;