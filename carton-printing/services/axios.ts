import axios from 'axios';

/**
 * Axios instance
 * @type {AxiosInstance}
 */
export const http = axios.create({
  baseURL: process.env.API_URL,
  timeout: 180000, // request timeout
  maxRedirects: 10, // follow up to 10 HTTP 3xx redirects
  headers: {},
});
