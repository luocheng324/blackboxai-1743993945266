<template>
  <div class="properties-panel">
    <h3>Properties</h3>
    <div v-if="selectedComponent" class="properties-form">
      <div class="form-group">
        <label>Component Type</label>
        <input :value="selectedComponent.type" disabled />
      </div>
      <div class="form-group">
        <label>Position X</label>
        <input type="number" v-model.number="selectedComponent.x" />
      </div>
      <div class="form-group">
        <label>Position Y</label>
        <input type="number" v-model.number="selectedComponent.y" />
      </div>
      <button @click="saveChanges">Save Changes</button>
    </div>
    <div v-else class="empty-state">
      Select a component to edit its properties
    </div>
  </div>
</template>

<script>
export default {
  props: {
    selectedComponent: Object
  },
  methods: {
    saveChanges() {
      this.$emit('update-component', this.selectedComponent)
    }
  }
}
</script>

<style scoped>
.properties-panel {
  padding: 1rem;
  background: #f5f5f5;
  height: 100%;
}

.properties-form {
  display: grid;
  gap: 1rem;
}

.form-group {
  display: grid;
  gap: 0.25rem;
}

.form-group label {
  font-weight: bold;
}

.empty-state {
  padding: 1rem;
  text-align: center;
  color: #666;
}
</style>