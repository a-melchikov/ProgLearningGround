import React, {useState, useEffect} from "react";
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
import {fetchTasks, fetchTaskDetails, executeTask} from "./api";
import {dracula} from "@uiw/codemirror-theme-dracula";
import {githubLight} from "@uiw/codemirror-theme-github";

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

const CodeExecutor = ({toggleTheme, theme}) => {
    const [code, setCode] = useState("");
    const [result, setResult] = useState("");
    const [taskName, setTaskName] = useState("");
    const [loading, setLoading] = useState(false);
    const [tasks, setTasks] = useState([]);
    const [taskDetails, setTaskDetails] = useState(null);
    const [language, setLanguage] = useState("en");

    const t = translations[language];

    useEffect(() => {
        const loadTasks = async () => {
            try {
                const tasks = await fetchTasks();
                setTasks(tasks);
            } catch (error) {
                console.error("Error fetching tasks:", error);
            }
        };

        loadTasks();
    }, []);

    const handleCodeChange = (value) => {
        setCode(value);
    };

    const handleTaskNameChange = async (e) => {
        const selectedTask = e.target.value;
        setTaskName(selectedTask);

        try {
            const details = await fetchTaskDetails(selectedTask);
            setTaskDetails(details);
        } catch (error) {
            console.error("Error fetching task details:", error);
        }
    };

    const handleSubmit = async () => {
        setLoading(true);
        setResult("");

        try {
            const result = await executeTask(taskName, code);
            setResult(result);
        } catch (error) {
            console.error("Error executing code:", error);
            setResult("Error executing code");
        } finally {
            setLoading(false);
        }
    };

    const toggleLanguage = () => {
        setLanguage((prevLanguage) => (prevLanguage === "en" ? "ru" : "en"));
    };

    return (
        <Box sx={{height: "100vh", overflow: "auto"}}>
            <AppBar position="static">
                <Toolbar>
                    <Typography variant="h6" sx={{flexGrow: 1}}>
                        {t.codeEditor}
                    </Typography>
                    <Button onClick={toggleLanguage} color="inherit">
                        {language === "en" ? "ru" : "en"}
                    </Button>
                    <IconButton onClick={toggleTheme} color="inherit">
                        {theme === "dark" ? <Brightness7/> : <Brightness4/>}
                    </IconButton>
                </Toolbar>
            </AppBar>

            <Paper
                sx={{
                    margin: 4,
                    padding: 6,
                    maxWidth: "800px",
                    display: "flex",
                    flexDirection: "column",
                    justifyContent: "center",
                    mx: "auto",
                    backgroundColor: theme === "dark" ? "#2e2e2e" : "#f9f9f9",
                    color: theme === "dark" ? "#fff" : "#000",
                }}
                elevation={3}
            >
                <Box sx={{display: "grid", gap: 2}}>
                    <FormControl fullWidth>
                        <InputLabel>{t.taskName}</InputLabel>
                        <Select
                            label={t.taskName}
                            value={taskName}
                            onChange={handleTaskNameChange}
                            disabled={loading}
                        >
                            {tasks.map((task, index) => (
                                <MenuItem key={index} value={task.name}>
                                    {task.name}
                                </MenuItem>
                            ))}
                        </Select>
                    </FormControl>

                    {taskDetails && (
                        <Box
                            sx={{
                                padding: 2,
                                borderRadius: 2,
                                border: `1px solid ${theme === "dark" ? "#444" : "#ccc"}`,
                                backgroundColor: theme === "dark" ? "#424242" : "#fff",
                            }}
                        >
                            <Typography
                                variant="h5"
                                sx={{
                                    mb: 2,
                                    color: theme === "dark" ? "#90caf9" : "inherit",
                                }}
                            >
                                {t.description}:
                            </Typography>
                            <Typography sx={{mb: 2}}>{taskDetails.description}</Typography>

                            <Box sx={{mb: 2}}>
                                <Typography
                                    variant="h6"
                                    sx={{color: theme === "dark" ? "#81c784" : "primary.main"}}
                                >
                                    {t.input}:
                                </Typography>
                                <Typography sx={{ml: 2, fontStyle: "italic"}}>
                                    {taskDetails.input}
                                </Typography>
                            </Box>

                            <Box sx={{mb: 2}}>
                                <Typography
                                    variant="h6"
                                    sx={{color: theme === "dark" ? "#81c784" : "primary.main"}}
                                >
                                    {t.output}:
                                </Typography>
                                <Typography sx={{ml: 2, fontStyle: "italic"}}>
                                    {taskDetails.output}
                                </Typography>
                            </Box>

                            <Typography
                                variant="h6"
                                sx={{
                                    color: theme === "dark" ? "#ffb74d" : "primary.main",
                                    mt: 2,
                                    mb: 1,
                                }}
                            >
                                {t.examples}:
                            </Typography>
                            {taskDetails.examples.map((example, index) => (
                                <Paper
                                    key={index}
                                    elevation={2}
                                    sx={{
                                        p: 2,
                                        mb: 1,
                                        backgroundColor: theme === "dark" ? "#333" : "#fff",
                                        color: theme === "dark" ? "#e0e0e0" : "#000",
                                    }}
                                >
                                    <Typography variant="body1">
                                        <strong>{t.input}:</strong> {example.input}
                                    </Typography>
                                    <Typography variant="body1">
                                        <strong>{t.output}:</strong> {example.output}
                                    </Typography>
                                </Paper>
                            ))}
                        </Box>
                    )}

                    <Typography variant="h6">{t.codeEditor}:</Typography>
                    <Box
                        sx={{
                            padding: 2,
                            borderRadius: 2,
                            border: `1px solid ${theme === "dark" ? "#444" : "#ccc"}`,
                            backgroundColor: theme === "dark" ? "#2e2e2e" : "#f9f9f9",
                        }}
                    >
                        <CodeMirror
                            value={code}
                            extensions={[python()]}
                            theme={theme === "dark" ? dracula : githubLight}
                            onChange={(value) => handleCodeChange(value)}
                            height="300px"
                        />
                    </Box>

                    <Box sx={{textAlign: "center"}}>
                        <Button
                            variant="contained"
                            onClick={handleSubmit}
                            disabled={loading || !code || !taskName}
                        >
                            {loading ? <CircularProgress size={24}/> : t.runCode}
                        </Button>
                    </Box>
                    <Box
                        sx={{
                            mt: 3,
                            textAlign: "center",
                            backgroundColor: "transparent",
                            color: result.includes("100.00%")
                                ? theme === "dark"
                                    ? "#4caf50"
                                    : "#388e3c"
                                : result.includes("0.00%")
                                    ? theme === "dark"
                                        ? "#ff5252"
                                        : "#d32f2f"
                                    : theme === "dark"
                                        ? "#ffa726"
                                        : "#f57c00",
                        }}
                    >
                        <Typography variant="h6" sx={{fontWeight: "bold"}}>
                            {result}
                        </Typography>
                    </Box>
                </Box>
            </Paper>
        </Box>
    );
};

export default CodeExecutor;
