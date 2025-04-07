<template>
  <div 
    class="workspace"
    @drop="onDrop"
    @dragover.prevent
  >
    <svg class="connections-layer">
      <line 
        v-for="(conn, index) in connections" 
        :key="index"
        :x1="conn.source.x + 25"
        :y1="conn.source.y + 25"
        :x2="conn.target.x + 25"
        :y2="conn.target.y + 25"
        stroke="#666"
        stroke-width="2"
      />
    </svg>
    <div 
      v-for="component in placedComponents" 
      :key="component.id"
      class="workspace-component"
      :style="{ left: `${component.x}px`, top: `${component.y}px` }"
    >
      <img 
        :src="`/components-SVG/${component.type.toLowerCase()}.svg`" 
        :class="{ 
          selected: component.id === selectedId,
          'connection-source': component.id === connectionSource
        }"
        @click="$emit('component-click', component.id)"
      />
    </div>
  </div>
</template>

<script>
export default {
  props: {
    selectedId: Number,
    placedComponents: Array,
    connections: Array,
    connectionSource: Number
  },
  data() {
    return {
      nextId: 1
    }
  },
  methods: {
    onDrop(event) {
      const type = event.dataTransfer.getData('component-type')
      const rect = event.currentTarget.getBoundingClientRect()
      const x = event.clientX - rect.left - 25
      const y = event.clientY - rect.top - 25
      
      const newComponent = {
        id: this.nextId++,
        type,
        x,
        y
      }
      this.$emit('place-component', newComponent)
    }
  }
}
</script>

<style scoped>
.workspace {
  position: relative;
  width: 100%;
  height: 100%;
  background: #f9f9f9;
  border: 1px dashed #ccc;
}

.workspace-component {
  position: absolute;
  width: 50px;
  height: 50px;
  cursor: move;
  z-index: 1;
}

.workspace-component img {
  width: 100%;
  height: 100%;
}

.workspace-component img.selected {
  outline: 2px solid #42b983;
}

.workspace-component img.connection-source {
  outline: 2px solid #3498db;
  animation: pulse 1.5s infinite;
}

.connections-layer {
  position: absolute;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 0;
}

@keyframes pulse {
  0% { outline-color: #3498db; }
  50% { outline-color: #42b983; }
  100% { outline-color: #3498db; }
}
</style>