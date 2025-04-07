<template>
  <div class="app-container">
    <header class="app-header">
      <h1>Oil Analysis System</h1>
      <div class="controls">
        <div v-if="executionStatus" class="status-message">
          {{ executionStatus }}
        </div>
        <button @click="saveAnalysis" class="save-btn">
          Save
        </button>
        <button @click="loadAnalysisList" class="load-btn">
          Load
        </button>
        <button 
          v-if="selectedAnalysis"
          @click="executeAnalysis" 
          class="execute-btn"
        >
          Execute
        </button>
      </div>
    </header>

    <!-- Analysis Selection Modal -->
    <div v-if="showAnalysisList" class="modal">
      <div class="modal-content">
        <h3>Select Analysis</h3>
        <ul class="analysis-list">
          <li 
            v-for="analysis in analyses" 
            :key="analysis.id"
            @click="loadAnalysis(analysis.id)"
          >
            {{ analysis.name || `Analysis ${analysis.id}` }}
            <span class="date">{{ formatDate(analysis.created_at) }}</span>
          </li>
        </ul>
        <button @click="showAnalysisList = false" class="cancel-btn">
          Cancel
        </button>
      </div>
    </div>

    <!-- Results Modal -->
    <div v-if="showResults" class="modal">
      <div class="modal-content">
        <h3>Analysis Results</h3>
        <div class="results-container">
          <div v-for="(result, index) in analysisResults" :key="index" class="result-item">
            <h4>{{ result.component }} ({{ result.type }})</h4>
            <div class="result-values">
              <div v-for="(value, key) in result.values" :key="key" class="value-row">
                <span class="value-label">{{ key }}:</span>
                <span class="value-data">{{ value }}</span>
              </div>
            </div>
          </div>
        </div>
        <button @click="showResults = false" class="cancel-btn">
          Close
        </button>
      </div>
    </div>

    <div class="main-content">
      <ComponentPalette />
      <Workspace 
        :selectedId="selectedId"
        :placedComponents="components"
        :connections="connections"
        :connectionSource="connectionSource"
        @component-click="handleComponentClick"
        @place-component="addComponent"
      />
      <PropertiesPanel 
        :selectedComponent="selectedComponent"
        @update-component="updateComponent"
      />
    </div>
  </div>
</template>

<script>
import ComponentPalette from './components/ComponentPalette.vue'
import Workspace from './components/Workspace.vue'
import PropertiesPanel from './components/PropertiesPanel.vue'
import api from './services/api'

export default {
  components: {
    ComponentPalette,
    Workspace,
    PropertiesPanel
  },
  data() {
    return {
      selectedId: null,
      components: [],
      connections: [],
      connectionMode: false,
      connectionSource: null,
      showAnalysisList: false,
      analyses: [],
      selectedAnalysis: null,
      showResults: false,
      analysisResults: [],
      executionStatus: null,
      pollInterval: null
    }
  },
  computed: {
    selectedComponent() {
      return this.components.find(c => c.id === this.selectedId)
    }
  },
  methods: {
    addComponent(component) {
      this.components.push(component)
      this.selectedId = component.id
    },
    updateComponent(updatedComponent) {
      const index = this.components.findIndex(c => c.id === updatedComponent.id)
      if (index !== -1) {
        this.components.splice(index, 1, updatedComponent)
      }
    },
    toggleConnectionMode() {
      this.connectionMode = !this.connectionMode
      this.connectionSource = null
    },
    handleComponentClick(id) {
      if (this.connectionMode) {
        if (!this.connectionSource) {
          this.connectionSource = id
        } else {
          this.createConnection(this.connectionSource, id)
          this.connectionSource = null
          this.connectionMode = false
        }
      } else {
        this.selectedId = id
      }
    },
    createConnection(sourceId, targetId) {
      const source = this.components.find(c => c.id === sourceId)
      const target = this.components.find(c => c.id === targetId)
      
      if (source && target) {
        this.connections.push({
          source,
          target
        })
      }
    },
    async saveAnalysis() {
      try {
        const analysis = {
          components: this.components,
          connections: this.connections
        }
        const response = await api.saveAnalysis(analysis)
        alert('Analysis saved successfully!')
        return response
      } catch (error) {
        console.error('Error saving analysis:', error)
        alert('Failed to save analysis')
        throw error
      }
    },
    async loadAnalysisList() {
      try {
        this.analyses = await api.getAnalysisList()
        this.showAnalysisList = true
      } catch (error) {
        console.error('Error loading analysis list:', error)
        alert('Failed to load analysis list')
        throw error
      }
    },
    async loadAnalysis(id) {
      try {
        const analysis = await api.loadAnalysis(id)
        this.components = analysis.components || []
        this.connections = analysis.connections || []
        this.showAnalysisList = false
        this.selectedAnalysis = id
      } catch (error) {
        console.error('Error loading analysis:', error)
        alert('Failed to load analysis')
        throw error
      }
    },
    async executeAnalysis() {
      try {
        this.executionStatus = 'Running analysis...'
        const response = await api.executeAnalysis(this.selectedAnalysis)
        
        // Start polling for results
        this.pollInterval = setInterval(async () => {
          try {
            const results = await api.getAnalysisResults(this.selectedAnalysis)
            if (results.status === 'COMPLETED') {
              clearInterval(this.pollInterval)
              this.executionStatus = null
              this.analysisResults = results.data
              this.showResults = true
            } else if (results.status === 'FAILED') {
              clearInterval(this.pollInterval)
              this.executionStatus = 'Analysis failed'
              throw new Error('Analysis execution failed')
            }
          } catch (error) {
            clearInterval(this.pollInterval)
            this.executionStatus = 'Error fetching results'
            console.error('Error polling results:', error)
            throw error
          }
        }, 2000)
        
        return response
      } catch (error) {
        this.executionStatus = 'Execution failed'
        console.error('Error executing analysis:', error)
        throw error
      }
    },
    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString()
    }
  },
  beforeUnmount() {
    if (this.pollInterval) {
      clearInterval(this.pollInterval)
    }
  }
}
</script>

<style>
body {
  margin: 0;
  font-family: Arial, sans-serif;
}

.app-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.app-header {
  padding: 1rem;
  background: #2c3e50;
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.controls {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.save-btn {
  background: #2ecc71;
}

.load-btn {
  background: #3498db;
}

.execute-btn {
  background: #e74c3c;
}

button {
  padding: 0.5rem 1rem;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  opacity: 0.9;
}

.status-message {
  padding: 0.5rem;
  background: #f39c12;
  color: white;
  border-radius: 4px;
  margin-right: 1rem;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 100;
}

.modal-content {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  max-width: 500px;
  width: 100%;
}

.analysis-list {
  list-style: none;
  padding: 0;
  max-height: 300px;
  overflow-y: auto;
}

.analysis-list li {
  padding: 0.5rem;
  border-bottom: 1px solid #eee;
  cursor: pointer;
}

.analysis-list li:hover {
  background: #f5f5f5;
}

.date {
  float: right;
  color: #777;
  font-size: 0.8rem;
}

.cancel-btn {
  margin-top: 1rem;
  background: #95a5a6;
}

.results-container {
  max-height: 60vh;
  overflow-y: auto;
  margin: 1rem 0;
}

.result-item {
  background: #f9f9f9;
  padding: 1rem;
  margin-bottom: 1rem;
  border-radius: 4px;
}

.value-row {
  display: flex;
  justify-content: space-between;
  margin: 0.5rem 0;
}

.value-label {
  font-weight: bold;
}

.value-data {
  color: #2c3e50;
}

.main-content {
  display: flex;
  flex: 1;
  overflow: hidden;
}

.main-content > * {
  flex: 1;
  padding: 1rem;
}
</style>