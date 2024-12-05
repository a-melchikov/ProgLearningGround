import React from "react";
import {Paper, Typography, Box, LinearProgress} from "@mui/material";
import CheckCircleIcon from "@mui/icons-material/CheckCircle";
import ErrorIcon from "@mui/icons-material/Error";
import WarningAmberIcon from "@mui/icons-material/WarningAmber";

const ResultCard = ({result}) => {
    const [passed, total] = result.match(/\d+/g).map(Number);
    const percentage = Math.round((passed / total) * 100);
    const isSuccess = percentage === 100;
    const isFailure = percentage === 0;

    const getColor = () => {
        if (isSuccess) return "success.main";
        if (isFailure) return "error.main";
        return "warning.main";
    };

    const getIcon = () => {
        if (isSuccess) return <CheckCircleIcon fontSize="large" sx={{color: "success.main"}}/>;
        if (isFailure) return <ErrorIcon fontSize="large" sx={{color: "error.main"}}/>;
        return <WarningAmberIcon fontSize="large" sx={{color: "warning.main"}}/>;
    };

    return (
        <Paper
            elevation={3}
            sx={{
                mt: 3,
                p: 3,
                borderRadius: 2,
                textAlign: "center",
                backgroundColor: isSuccess
                    ? "success.light"
                    : isFailure
                        ? "error.light"
                        : "warning.light",
            }}
        >
            <Box sx={{display: "flex", justifyContent: "center", alignItems: "center", mb: 2}}>
                {getIcon()}
            </Box>
            <Typography variant="h6" sx={{fontWeight: "bold", color: getColor()}}>
                {passed} из {total} тестов пройдено ({percentage}%).
            </Typography>
            {!isSuccess && (
                <Box sx={{mt: 2}}>
                    <LinearProgress
                        variant="determinate"
                        value={percentage}
                        sx={{
                            height: 10,
                            borderRadius: 5,
                            backgroundColor: "grey.300",
                            "& .MuiLinearProgress-bar": {backgroundColor: getColor()},
                        }}
                    />
                </Box>
            )}
        </Paper>
    );
};

export default ResultCard;
