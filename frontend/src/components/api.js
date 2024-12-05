import axios from "axios";

const BASE_URL = "http://localhost:8000/api/v1/tasks/";

export const fetchTasks = async () => {
    const response = await axios.get(`${BASE_URL}names`);
    return response.data;
};

export const fetchTaskDetails = async (taskName) => {
    const response = await axios.get(`${BASE_URL}${taskName}`);
    return response.data;
};

export const executeTask = async (taskName, code) => {
    const response = await axios.post(`${BASE_URL}send_task/${taskName}`, {code});
    return response.data.result;
};
