import React, {useState} from "react";
import axios from "axios";
import {
    TextField,
    Button,
    Typography,
    Paper,
    CircularProgress,
    Grid
} from "@mui/material";

const CodeExecutor = () => {
    const [code, setCode] = useState("");
    const [result, setResult] = useState("");
    const [taskName, setTaskName] = useState("");
    const [loading, setLoading] = useState(false);

    const handleCodeChange = (e) => {
        setCode(e.target.value);
    };

    const handleTaskNameChange = (e) => {
        setTaskName(e.target.value);
    };

    const handleSubmit = async () => {
        setLoading(true);
        setResult("");

        try {
            const response = await axios.post(
                `http://localhost:8000/send_task/${taskName}/`,
                {code: code}
            );
            setResult(response.data.result);
        } catch (error) {
            console.error("Error executing code:", error);
            setResult("Error executing code");
        } finally {
            setLoading(false);
        }
    };

    return (
        <Paper sx={{padding: 4}} elevation={3}>
            <Grid container spacing={2}>
                <Grid item xs={12}>
                    <Typography variant="h5" align="center" gutterBottom>
                        Enter your code and task
                    </Typography>
                </Grid>

                <Grid item xs={12}>
                    <TextField
                        label="Task Name"
                        fullWidth
                        variant="outlined"
                        value={taskName}
                        onChange={handleTaskNameChange}
                    />
                </Grid>

                <Grid item xs={12}>
                    <TextField
                        label="Code"
                        fullWidth
                        multiline
                        minRows={10}
                        variant="outlined"
                        value={code}
                        onChange={handleCodeChange}
                    />
                </Grid>

                <Grid item xs={12} sx={{textAlign: "center"}}>
                    <Button
                        variant="contained"
                        color="primary"
                        onClick={handleSubmit}
                        disabled={loading || !code || !taskName}
                    >
                        {loading ? (
                            <CircularProgress size={24} sx={{color: "white"}}/>
                        ) : (
                            "Run Code"
                        )}
                    </Button>
                </Grid>

                <Grid item xs={12}>
                    <Typography variant="h6" gutterBottom>
                        Result:
                    </Typography>
                    <pre>{result}</pre>
                </Grid>
            </Grid>
        </Paper>
    );
};

export default CodeExecutor;
