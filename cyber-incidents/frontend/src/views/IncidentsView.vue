<template>
  <div class="incidents-container">
    <header>
      <h1>Security Incidents</h1>
      <div>
        <span>Welcome, {{ username }}</span>
        <button @click="handleLogout" class="logout-btn">Logout</button>
      </div>
    </header>
    
    <div class="incidents-actions">
      <button @click="showAddModal = true" class="add-btn">Add Incident</button>
    </div>
    
    <table class="incidents-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Title</th>
          <th>Severity</th>
          <th>Status</th>
          <th>Reporter</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="incident in incidents" :key="incident.id">
          <td>{{ incident.id }}</td>
          <td>{{ incident.title }}</td>
          <td :class="`severity-${incident.severity}`">{{ incident.severity }}</td>
          <td>{{ incident.status }}</td>
          <td>{{ incident.reporter }}</td>
          <td>
            <button @click="openEditModal(incident)" class="edit-btn">Edit</button>
          </td>
        </tr>
      </tbody>
    </table>
    
    <!-- Add Incident Modal -->
    <div v-if="showAddModal" class="modal">
      <div class="modal-content">
        <span class="close" @click="showAddModal = false">&times;</span>
        <h2>Add New Incident</h2>
        <form @submit.prevent="addIncident">
          <div class="form-group">
            <label>Title</label>
            <input v-model="newIncident.title" required>
          </div>
          <div class="form-group">
            <label>Description</label>
            <textarea v-model="newIncident.description" required></textarea>
          </div>
          <div class="form-group">
            <label>Severity</label>
            <select v-model="newIncident.severity" required>
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
              <option value="critical">Critical</option>
            </select>
          </div>
          <div class="form-group">
            <label>Status</label>
            <select v-model="newIncident.status" required>
              <option value="open">Open</option>
              <option value="in_progress">In Progress</option>
              <option value="resolved">Resolved</option>
            </select>
          </div>
          <button type="submit" :disabled="loading">
            <span v-if="loading" class="spinner"></span>
            <span v-else>Add Incident</span>
          </button>
        </form>
      </div>
    </div>
    
    <!-- Edit Incident Modal -->
    <div v-if="showEditModal" class="modal">
      <div class="modal-content">
        <span class="close" @click="showEditModal = false">&times;</span>
        <h2>Edit Incident</h2>
        <form @submit.prevent="updateIncident">
          <div class="form-group">
            <label>Title</label>
            <input v-model="editingIncident.title" required>
          </div>
          <div class="form-group">
            <label>Description</label>
            <textarea v-model="editingIncident.description" required></textarea>
          </div>
          <div class="form-group">
            <label>Severity</label>
            <select v-model="editingIncident.severity" required>
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
              <option value="critical">Critical</option>
            </select>
          </div>
          <div class="form-group">
            <label>Status</label>
            <select v-model="editingIncident.status" required>
              <option value="open">Open</option>
              <option value="in_progress">In Progress</option>
              <option value="resolved">Resolved</option>
            </select>
          </div>
          <button type="submit" :disabled="loading">
            <span v-if="loading" class="spinner"></span>
            <span v-else>Update Incident</span>
          </button>
        </form>
      </div>
    </div>
    
    <div v-if="loading" class="loading-overlay">
      <div class="spinner"></div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      incidents: [],
      username: localStorage.getItem('username') || '',
      showAddModal: false,
      showEditModal: false,
      loading: false,
      newIncident: {
        title: '',
        description: '',
        severity: 'medium',
        status: 'open'
      },
      editingIncident: {
        id: null,
        title: '',
        description: '',
        severity: 'medium',
        status: 'open'
      }
    }
  },
  async created() {
    await this.fetchIncidents()
  },
  methods: {
    async fetchIncidents() {
      this.loading = true
      try {
        const auth = localStorage.getItem('auth')
        const response = await fetch('http://localhost:5000/incidents', {
          headers: {
            'Authorization': `Basic ${auth}`
          }
        })
        
        if (response.ok) {
          this.incidents = await response.json()
        } else {
          this.handleLogout()
        }
      } catch (error) {
        console.error('Error fetching incidents:', error)
        this.handleLogout()
      } finally {
        this.loading = false
      }
    },
    async addIncident() {
      this.loading = true
      try {
        const auth = localStorage.getItem('auth')
        const response = await fetch('http://localhost:5000/incidents', {
          method: 'POST',
          headers: {
            'Authorization': `Basic ${auth}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(this.newIncident)
        })
        
        if (response.ok) {
          this.showAddModal = false
          this.newIncident = {
            title: '',
            description: '',
            severity: 'medium',
            status: 'open'
          }
          await this.fetchIncidents()
        }
      } catch (error) {
        console.error('Error adding incident:', error)
      } finally {
        this.loading = false
      }
    },
    openEditModal(incident) {
      this.editingIncident = { ...incident }
      this.showEditModal = true
    },
    async updateIncident() {
      this.loading = true
      try {
        const auth = localStorage.getItem('auth')
        const response = await fetch(`http://localhost:5000/incidents/${this.editingIncident.id}`, {
          method: 'PUT',
          headers: {
            'Authorization': `Basic ${auth}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(this.editingIncident)
        })
        
        if (response.ok) {
          this.showEditModal = false
          await this.fetchIncidents()
        }
      } catch (error) {
        console.error('Error updating incident:', error)
      } finally {
        this.loading = false
      }
    },
    handleLogout() {
      localStorage.removeItem('auth')
      localStorage.removeItem('username')
      this.$router.push('/')
    }
  }
}
</script>

<style scoped>
.incidents-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.logout-btn {
  background-color: #f44336;
  color: white;
  padding: 5px 10px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-left: 10px;
}

.incidents-actions {
  margin-bottom: 20px;
}

.add-btn {
  background-color: #4CAF50;
  color: white;
  padding: 10px 15px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.incidents-table {
  width: 100%;
  border-collapse: collapse;
}

.incidents-table th, .incidents-table td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

.incidents-table th {
  background-color: #f2f2f2;
}

.incidents-table tr:nth-child(even) {
  background-color: #f9f9f9;
}

.edit-btn {
  background-color: #2196F3;
  color: white;
  padding: 5px 10px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.severity-low {
  color: green;
  font-weight: bold;
}

.severity-medium {
  color: orange;
  font-weight: bold;
}

.severity-high {
  color: red;
  font-weight: bold;
}

.severity-critical {
  color: darkred;
  font-weight: bold;
}

.modal {
  position: fixed;
  z-index: 1;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0,0,0,0.4);
}

.modal-content {
  background-color: #fefefe;
  margin: 15% auto;
  padding: 20px;
  border: 1px solid #888;
  width: 50%;
  border-radius: 5px;
}

.close {
  color: #aaa;
  float: right;
  font-size: 28px;
  font-weight: bold;
  cursor: pointer;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
}

.form-group input, .form-group textarea, .form-group select {
  width: 100%;
  padding: 8px;
  box-sizing: border-box;
}

.form-group textarea {
  height: 100px;
}

button[type="submit"] {
  background-color: #4CAF50;
  color: white;
  padding: 10px 15px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  position: relative;
}

.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(255, 255, 255, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 5px solid rgba(0, 0, 0, 0.1);
  border-radius: 50%;
  border-top-color: #42b983;
  animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>