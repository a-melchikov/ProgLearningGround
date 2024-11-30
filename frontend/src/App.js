import React from "react";
import CodeExecutor from "./components/CodeExecutor";
import {CssBaseline} from "@mui/material";

function App() {
    return (
        <div className="App">
            <CssBaseline/>
            <CodeExecutor/>
        </div>
    );
}

export default App;
