

import axios from 'axios';

const API_BASE_URL = 'https://altogpt.onrender.com';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});


export const askAI = async (query) => {
  const response = await api.post('/query/', { query });
  return response.data.response;
};


export const getBuildingStatus = async () => {
  const response = await api.get('/buildings/building_1/status/');
  return response.data.status;
};

export default api;
