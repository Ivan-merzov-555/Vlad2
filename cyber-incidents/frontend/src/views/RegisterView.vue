<template>
  <div class="register-container">
    <h1>Register</h1>
    <form @submit.prevent="handleRegister">
      <div class="form-group">
        <label for="username">Username</label>
        <input 
          v-model="form.username" 
          type="text" 
          id="username" 
          required
          @input="validateUsername"
        >
        <p class="error" v-if="errors.username">{{ errors.username }}</p>
      </div>
      <div class="form-group">
        <label for="password">Password</label>
        <input 
          v-model="form.password" 
          type="password" 
          id="password" 
          required
          @input="validatePassword"
        >
        <p class="error" v-if="errors.password">{{ errors.password }}</p>
      </div>
      <button type="submit" :disabled="!isFormValid || loading">
        <span v-if="loading" class="spinner"></span>
        <span v-else>Register</span>
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
      errors: {
        username: '',
        password: ''
      },
      loading: false,
      error: ''
    }
  },
  computed: {
    isFormValid() {
      return this.form.username && !this.errors.username && 
             this.form.password && !this.errors.password
    }
  },
  methods: {
    validateUsername() {
      if (!this.form.username) {
        this.errors.username = 'Username is required'
      } else if (this.form.username.length < 3) {
        this.errors.username = 'Username must be at least 3 characters'
      } else if (!/^[a-zA-Z0-9_]+$/.test(this.form.username)) {
        this.errors.username = 'Username can only contain letters, numbers and underscores'
      } else {
        this.errors.username = ''
      }
    },
    validatePassword() {
      if (!this.form.password) {
        this.errors.password = 'Password is required'
      } else if (this.form.password.length < 6) {
        this.errors.password = 'Password must be at least 6 characters'
      } else {
        this.errors.password = ''
      }
    },
    async handleRegister() {
      this.validateUsername()
      this.validatePassword()
      
      if (!this.isFormValid) return
      
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
  position: relative;
}

button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.error {
  color: red;
  font-size: 0.8rem;
  margin-top: 0.25rem;
}

.spinner {
  display: inline-block;
  width: 20px;
  height: 20px;
  border: 3px solid rgba(255,255,255,.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>