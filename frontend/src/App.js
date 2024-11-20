import React from "react";
import CodeExecutor from "./components/CodeExecutor";
import {Container, CssBaseline, Typography} from "@mui/material";

function App() {
    return (
        <div className="App">
            <CssBaseline/>
            <Container maxWidth="sm">
                <header className="App-header">
                    <Typography variant="h3" align="center" gutterBottom>
                        Code Executor
                    </Typography>
                    <CodeExecutor/>
                </header>
            </Container>
        </div>
    );
}

export default App;
