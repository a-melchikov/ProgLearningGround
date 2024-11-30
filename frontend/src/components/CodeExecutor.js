import React, {useState, useEffect} from "react";
import axios from "axios";
import {
    Button,
    Typography,
    Paper,
    CircularProgress,
    MenuItem,
    Select,
    InputLabel,
    FormControl,
    Box,
    AppBar,
    Toolbar,
    IconButton,
} from "@mui/material";
import CodeMirror from "@uiw/react-codemirror";
import {python} from "@codemirror/lang-python";
import {Brightness4, Brightness7} from "@mui/icons-material";

const translations = {
    en: {
        taskName: "Task Name",
        description: "Description",
        input: "Input",
        output: "Output",
        examples: "Examples",
        codeEditor: "Code Editor",
        runCode: "Run Code",
        result: "Result",
    },
    ru: {
        taskName: "Название задания",
        description: "Описание",
        input: "Ввод",
        output: "Вывод",
        examples: "Примеры",
        codeEditor: "Редактор кода",
        runCode: "Запустить код",
        result: "Результат",
    },
};

const CodeExecutor = () => {
    const [code, setCode] = useState("");
    const [result, setResult] = useState("");
    const [taskName, setTaskName] = useState("");
    const [loading, setLoading] = useState(false);
    const [tasks, setTasks] = useState([]);
    const [taskDetails, setTaskDetails] = useState(null);
    const [theme, setTheme] = useState("dark");
    const [language, setLanguage] = useState("en");

    const t = translations[language];

    useEffect(() => {
        const fetchTasks = async () => {
            try {
                const response = await axios.get("http://localhost:8000/api/v1/tasks/");
                setTasks(response.data);
            } catch (error) {
                console.error("Error fetching tasks:", error);
            }
        };

        fetchTasks();
    }, []);

    const handleCodeChange = (value) => {                                        // Стиль для выбранного элемента

        setCode(value);
    };

    const handleTaskNameChange = async (e) => {
        const selectedTask = e.target.value;
        setTaskName(selectedTask);

        try {
            const response = await axios.get(
                `http://localhost:8000/api/v1/tasks/${selectedTask}/`
            );
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
                `http://localhost:8000/api/v1/tasks/send_task/${taskName}/`,
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

    const toggleTheme = () => {
        setTheme((prevTheme) => (prevTheme === "dark" ? "light" : "dark"));
    };

    const toggleLanguage = () => {
        setLanguage((prevLanguage) => (prevLanguage === "en" ? "ru" : "en"));
    };

    return (
        <Box
            sx={{
                height: "100vh",
                bgcolor: theme === "dark" ? "#121212" : "#f9f9f9",
                color: theme === "dark" ? "#fff" : "#000",
                overflow: "auto",
            }}
        >
            <AppBar position="static" sx={{bgcolor: theme === "dark" ? "#333" : "#fff"}}>
                <Toolbar>
                    <Box sx={{flexGrow: 1}}/>
                    <Box sx={{display: "flex", gap: 1}}>
                        <Button onClick={toggleLanguage} sx={{color: theme === "dark" ? "#fff" : "#000"}}>
                            {language === "en" ? "ru" : "en"}
                        </Button>
                        <IconButton onClick={toggleTheme} sx={{color: theme === "dark" ? "#fff" : "#000"}}>
                            {theme === "dark" ? <Brightness7/> : <Brightness4/>}
                        </IconButton>
                    </Box>
                </Toolbar>
            </AppBar>

            <Paper
                sx={{
                    margin: 4,
                    padding: 6,
                    maxWidth: "800px",
                    bgcolor: theme === "dark" ? "#1e1e1e" : "#fff",
                    color: theme === "dark" ? "#fff" : "#000",
                    display: "flex",
                    flexDirection: "column",
                    justifyContent: "center",
                    mx: "auto",
                }}
                elevation={3}
            >
                <Box sx={{display: "grid", gap: 2}}>
                    <FormControl fullWidth variant="outlined">
                        <InputLabel sx={{color: theme === "dark" ? "#fff" : "#000"}}>
                            {t.taskName}
                        </InputLabel>
                        <Select
                            label={t.taskName}
                            value={taskName}
                            onChange={handleTaskNameChange}
                            disabled={loading}
                            sx={{
                                "& .MuiOutlinedInput-notchedOutline": {
                                    borderColor: theme === "dark" ? "#fff" : "#000",
                                },
                                "& .MuiSvgIcon-root": {
                                    color: theme === "dark" ? "#fff" : "#000",
                                },
                                bgcolor: theme === "dark" ? "#333" : "#fff",
                                color: theme === "dark" ? "#fff" : "#000",
                                "& .MuiMenuItem-root": {
                                    backgroundColor: theme === "dark" ? "#444" : "#fff",
                                    color: theme === "dark" ? "#fff" : "#000",
                                    "&:hover": {
                                        backgroundColor: theme === "dark" ? "#555" : "#f0f0f0",
                                    },
                                },
                            }}
                        >
                            {tasks.map((task, index) => (
                                <MenuItem
                                    key={index}
                                    value={task.name}
                                    sx={{
                                        backgroundColor: theme === "dark" ? "#444" : "#fff",
                                        color: theme === "dark" ? "#fff" : "#000",
                                        "&:hover": {
                                            backgroundColor: theme === "dark" ? "#555" : "#f0f0f0",
                                        },
                                        "&.Mui-selected": {
                                            backgroundColor: theme === "dark" ? "#666" : "#dcdcdc",
                                            color: theme === "dark" ? "#fff" : "#000",
                                            "&:hover": {
                                                backgroundColor: theme === "dark" ? "#666" : "#dcdcdc",
                                            },
                                        },
                                    }}
                                    selected={task.name === taskName}
                                >
                                    {task.name}
                                </MenuItem>
                            ))}
                        </Select>
                    </FormControl>

                    {taskDetails && (
                        <Box
                            sx={{
                                padding: 2,
                                bgcolor: theme === "dark" ? "#333" : "#f4f4f4",
                                color: theme === "dark" ? "#fff" : "#000",
                                borderRadius: 2,
                                boxShadow: theme === "dark" ? "0px 2px 10px rgba(0, 0, 0, 0.5)" : "0px 2px 10px rgba(0, 0, 0, 0.1)",
                            }}
                        >
                            <Typography variant="h6">{t.description}:</Typography>
                            <Typography>{taskDetails.description}</Typography>
                            <Typography variant="h6" sx={{mt: 2}}>
                                {t.input}:
                            </Typography>
                            <Typography>{taskDetails.input}</Typography>
                            <Typography variant="h6" sx={{mt: 2}}>
                                {t.output}:
                            </Typography>
                            <Typography>{taskDetails.output}</Typography>
                            <Typography variant="h6" sx={{mt: 2}}>
                                {t.examples}:
                            </Typography>
                            {taskDetails.examples.map((example, index) => (
                                <Box
                                    key={index}
                                    sx={{
                                        mb: 1,
                                        bgcolor: theme === "dark" ? "#444" : "#fff",
                                        color: theme === "dark" ? "#fff" : "#000",
                                        padding: 1,
                                        borderRadius: 1,
                                        boxShadow: theme === "dark" ? "0px 1px 5px rgba(0, 0, 0, 0.5)" : "0px 1px 5px rgba(0, 0, 0, 0.1)",
                                    }}
                                >
                                    <Typography variant="body1">
                                        <strong>{t.input}:</strong> {example.input}
                                    </Typography>
                                    <Typography variant="body1">
                                        <strong>{t.output}:</strong> {example.output}
                                    </Typography>
                                </Box>
                            ))}
                        </Box>
                    )}

                    <Typography variant="h6">{t.codeEditor}:</Typography>
                    <CodeMirror
                        value={code}
                        extensions={[python()]}
                        onChange={(value) => handleCodeChange(value)}
                        height="300px"
                        theme={theme}
                    />

                    <Box sx={{textAlign: "center"}}>
                        <Button
                            variant="contained"
                            onClick={handleSubmit}
                            disabled={loading || !code || !taskName}
                            sx={{
                                bgcolor: theme === "dark" ? "#6200ea" : "#1976d2",
                                color: theme === "dark" ? "#fff" : "#000",
                                "&:hover": {
                                    bgcolor: theme === "dark" ? "#3700b3" : "#1565c0",
                                },
                                boxShadow: theme === "dark" ? "0px 4px 6px rgba(0, 0, 0, 0.6)" : "0px 4px 6px rgba(0, 0, 0, 0.2)",
                            }}
                        >
                            {loading ? <CircularProgress size={24} sx={{color: "#fff"}}/> : t.runCode}
                        </Button>

                    </Box>
                    <Typography variant="h6">{t.result}:</Typography>
                    <pre>{result}</pre>
                </Box>
            </Paper>
        </Box>
    );
};

export default CodeExecutor;
