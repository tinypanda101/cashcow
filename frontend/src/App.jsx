import { useEffect, useState } from "react";
import { Button, Typography, Box } from "@mui/material";
import './App.css'

function App() {
  const [msg, setMsg] = useState("not called yet");

  useEffect(() => {
    fetch("http://localhost:8000/health")
      .then((r) => r.json())
      .then((d) => setMsg(d.status))
      .catch((e) => setMsg("ERROR: " + e.message));
  }, []);

  return (
    <Box sx={{ p: 4 }}>
      <Typography variant="h4">CashCow</Typography>
      <Typography>Backend says: {msg}</Typography>
      <Button variant="contained">MUI works</Button>
    </Box>
  );
}
export default App;
    