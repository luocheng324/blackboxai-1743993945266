import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:8000/api/',
  timeout: 10000 // Increased timeout
})

// Request interceptor for logging
api.interceptors.request.use(config => {
  console.log(`[API] Request to ${config.method.toUpperCase()} ${config.url}`)
  return config
}, error => {
  console.error('[API] Request error:', error)
  return Promise.reject(error)
})

// Response interceptor for logging
api.interceptors.response.use(response => {
  console.log(`[API] Response from ${response.config.url}`, response.status)
  return response
}, error => {
  if (error.response) {
    console.error(
      '[API] Response error:',
      error.response.status,
      error.response.data
    )
  } else {
    console.error('[API] Network error:', error.message)
  }
  return Promise.reject(error)
})

export default {
  async saveAnalysis(components, connections) {
    try {
      const response = await api.post('/analysis/', {
        components,
        connections
      })
      return response.data
    } catch (error) {
      throw new Error(`Failed to save analysis: ${error.message}`)
    }
  },

  async loadAnalysis(id) {
    try {
      const response = await api.get(`/analysis/${id}/`)
      return response.data
    } catch (error) {
      throw new Error(`Failed to load analysis: ${error.message}`)
    }
  },

  async getAnalysisList() {
    try {
      const response = await api.get('/analysis/')
      return response.data
    } catch (error) {
      throw new Error(`Failed to get analysis list: ${error.message}`)
    }
  },

  async executeAnalysis(id) {
    try {
      const response = await api.post(`/analysis/${id}/execute/`, null, {
        timeout: 30000 // Longer timeout for execution
      })
      return response.data
    } catch (error) {
      throw new Error(`Analysis execution failed: ${error.message}`)
    }
  },

  async getAnalysisResults(id) {
    try {
      const response = await api.get(`/analysis/${id}/results/`)
      return response.data
    } catch (error) {
      throw new Error(`Failed to get results: ${error.message}`)
    }
  },

  async generateReport(id) {
    try {
      const response = await api.get(`/analysis/${id}/report/`, {
        responseType: 'blob',
        timeout: 15000
      })
      
      if (!response.data || response.data.size === 0) {
        throw new Error('Empty report generated')
      }
      
      return response.data
    } catch (error) {
      throw new Error(`Report generation failed: ${error.message}`)
    }
  },

  async getComponentTypes() {
    try {
      const response = await api.get('/components/')
      return response.data
    } catch (error) {
      throw new Error(`Failed to get component types: ${error.message}`)
    }
  }
}