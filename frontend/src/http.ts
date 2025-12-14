import axios from 'axios'

const base = (import.meta as any).env?.VITE_API_BASE || '/api'
const http = axios.create({ baseURL: base })
http.interceptors.request.use(cfg => {
  const t = localStorage.getItem('token')
  if (t) cfg.headers = { ...(cfg.headers||{}), Authorization: `Bearer ${t}` }
  return cfg
})

export default http
