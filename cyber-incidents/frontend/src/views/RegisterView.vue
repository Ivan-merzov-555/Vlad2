<template>
    <div class="register-container">
      <h1>Register</h1>
      <form @submit.prevent="handleRegister">
        <div class="form-group">
          <label for="username">Username</label>
          <input v-model="form.username" type="text" id="username" required>
        </div>
        <div class="form-group">
          <label for="password">Password</label>
          <input v-model="form.password" type="password" id="password" required>
        </div>
        <button type="submit" :disabled="loading">
          {{ loading ? 'Processing...' : 'Register' }}
        </button>
        <p v-if="error" class="error">{{ error }}</p>
        <p>Already have an account? <router-link to="/">Login</router-link></p>
      </form>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        form: {
          username: '',
          password: ''
        },
        loading: false,
        error: ''
      }
    },
    methods: {
      async handleRegister() {
        this.loading = true
        this.error = ''
        
        try {
          const response = await fetch('http://localhost:5000/register', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(this.form)
          })
  
          const data = await response.json()
          
          if (!response.ok) {
            throw new Error(data.error || 'Registration failed')
          }
  
          alert('Registration successful! Please login.')
          this.$router.push('/')
        } catch (err) {
          console.error('Registration error:', err)
          this.error = err.message || 'Registration failed'
        } finally {
          this.loading = false
        }
      }
    }
  }
  </script>
  
  <style scoped>
  .register-container {
    max-width: 400px;
    margin: 2rem auto;
    padding: 2rem;
    border: 1px solid #ddd;
    border-radius: 8px;
  }
  
  .form-group {
    margin-bottom: 1rem;
  }
  
  label {
    display: block;
    margin-bottom: 0.5rem;
  }
  
  input {
    width: 100%;
    padding: 0.5rem;
    font-size: 1rem;
    border: 1px solid #ddd;
    border-radius: 4px;
  }
  
  button {
    background-color: #42b983;
    color: white;
    padding: 0.5rem 1rem;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 1rem;
  }
  
  button:disabled {
    background-color: #cccccc;
    cursor: not-allowed;
  }
  
  .error {
    color: red;
    margin-top: 1rem;
  }
  </style>