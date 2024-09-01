// write interceptor for dealing with correct headers
import axios from 'axios';
import { ACCESS_TOKEN } from './constants';

const api = axios.create({
  baseURL: 'http://localhost:8000', // "https://dual3243242.azurewebsites.net" //"https://0.0.0.0:8000" //process.env.API_URL, // import anything inside .env
});

function getCookie(name: string): string {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + '=') {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

/*
This creates an api which can be used to do api calls and automatically wrap
them with correct access token. localStorage holds this token?
*/
api.interceptors.request.use(
  (config) => {
    //const token = localStorage.getItem(ACCESS_TOKEN);
    // if (token) {
    //   config.headers.Authorization = `Bearer ${token}`;
    // }
    const csrfToken = getCookie('csrftoken');
    if (csrfToken) {
      config.headers['X-CSRFToken'] = csrfToken; // token name dependent on backend
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  },
);
export default api;
