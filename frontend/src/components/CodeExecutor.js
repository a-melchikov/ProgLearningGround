import React, {useState, useEffect} from "react";
import axios from "axios";
import {
    TextField,
    Button,
    Typography,
    Paper,
    CircularProgress,
    Grid,
    MenuItem,
    Select,
    InputLabel,
    FormControl,
    Box,
} from "@mui/material";

const CodeExecutor = () => {
    const [code, setCode] = useState("");
    const [result, setResult] = useState("");
    const [taskName, setTaskName] = useState("");
    const [loading, setLoading] = useState(false);
    const [tasks, setTasks] = useState([]);
    const [taskDetails, setTaskDetails] = useState(null);

    useEffect(() => {
        const fetchTasks = async () => {
            try {
                const response = await axios.get("http://localhost:8000/tasks/");
                setTasks(response.data);
            } catch (error) {
                console.error("Error fetching tasks:", error);
            }
        };

        fetchTasks();
    }, []);

    const handleCodeChange = (e) => {
        setCode(e.target.value);
    };

    const handleTaskNameChange = async (e) => {
        const selectedTask = e.target.value;
        setTaskName(selectedTask);

        try {
            const response = await axios.get(`http://localhost:8000/task_details/${selectedTask}/`);
            setTaskDetails(response.data);
        } catch (error) {
            console.error("Error fetching task details:", error);
        }
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
                    <FormControl fullWidth variant="outlined">
                        <InputLabel>Task Name</InputLabel>
                        <Select
                            label="Task Name"
                            value={taskName}
                            onChange={handleTaskNameChange}
                            disabled={loading}
                        >
                            {tasks.map((task, index) => (
                                <MenuItem key={index} value={task}>
                                    {task}
                                </MenuItem>
                            ))}
                        </Select>
                    </FormControl>
                </Grid>

                {taskDetails && (
                    <Grid item xs={12}>
                        <Box sx={{padding: 2, backgroundColor: "#f4f4f4", borderRadius: 2}}>
                            <Typography variant="h6">Description:</Typography>
                            <Typography>{taskDetails.description}</Typography>

                            <Typography variant="h6" sx={{mt: 2}}>Input:</Typography>
                            <Typography>{taskDetails.input}</Typography>

                            <Typography variant="h6" sx={{mt: 2}}>Output:</Typography>
                            <Typography>{taskDetails.output}</Typography>

                            <Typography variant="h6" sx={{mt: 2}}>Examples:</Typography>
                            {taskDetails.examples.map((example, index) => (
                                <Box key={index} sx={{mb: 1}}>
                                    <Typography variant="body1">
                                        <strong>Input:</strong> {example.input}
                                    </Typography>
                                    <Typography variant="body1">
                                        <strong>Output:</strong> {example.output}
                                    </Typography>
                                </Box>
                            ))}
                        </Box>
                    </Grid>
                )}

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
