<template>
  <div class="login-container">
    <h1>Login</h1>
    <form @submit.prevent="handleLogin">
      <div class="form-group">
        <label for="username">Username</label>
        <input 
          v-model="username" 
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
          v-model="password" 
          type="password" 
          id="password" 
          required
          @input="validatePassword"
        >
        <p class="error" v-if="errors.password">{{ errors.password }}</p>
      </div>
      <button type="submit" :disabled="!isFormValid || loading">
        <span v-if="loading" class="spinner"></span>
        <span v-else>Login</span>
      </button>
      <p class="error" v-if="errorMessage">{{ errorMessage }}</p>
      <p>Don't have an account? <router-link to="/register">Register</router-link></p>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: '',
      password: '',
      errors: {
        username: '',
        password: ''
      },
      errorMessage: '',
      loading: false
    }
  },
  computed: {
    isFormValid() {
      return this.username && !this.errors.username && 
             this.password && !this.errors.password
    }
  },
  methods: {
    validateUsername() {
      if (!this.username) {
        this.errors.username = 'Username is required'
      } else if (this.username.length < 3) {
        this.errors.username = 'Username must be at least 3 characters'
      } else {
        this.errors.username = ''
      }
    },
    validatePassword() {
      if (!this.password) {
        this.errors.password = 'Password is required'
      } else if (this.password.length < 6) {
        this.errors.password = 'Password must be at least 6 characters'
      } else {
        this.errors.password = ''
      }
    },
    async handleLogin() {
      this.loading = true
      this.validateUsername()
      this.validatePassword()
      
      if (!this.isFormValid) {
        this.loading = false
        return
      }
      
      try {
        const auth = btoa(`${this.username}:${this.password}`);
        const response = await fetch('/api/incidents', {
          headers: {
            'Authorization': `Basic ${auth}`
          }
        });
        
        if (response.ok) {
          localStorage.setItem('auth', auth);
          this.$router.push('/incidents');
        } else {
          throw new Error('Invalid credentials');
        }
      } catch (error) {
        console.error('Login error:', error);
        this.errorMessage = 'Login failed. Check your credentials.';
      } finally {
        this.loading = false;
      }
    }
  }
}
</script>

<style scoped>
.login-container {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
  margin-top: 50px;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
}

input {
  width: 100%;
  padding: 8px;
  box-sizing: border-box;
}

button {
  background-color: #42b983;
  color: white;
  padding: 10px 15px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  position: relative;
}

button:hover {
  background-color: #369f6b;
}

button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.error {
  color: red;
  font-size: 0.8rem;
  margin-top: 5px;
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