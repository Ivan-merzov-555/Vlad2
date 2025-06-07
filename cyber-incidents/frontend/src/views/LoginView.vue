<template>
    <div class="login-container">
      <h1>Login</h1>
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="username">Username</label>
          <input v-model="username" type="text" id="username" required>
        </div>
        <div class="form-group">
          <label for="password">Password</label>
          <input v-model="password" type="password" id="password" required>
        </div>
        <button type="submit">Login</button>
        <p>Don't have an account? <router-link to="/register">Register</router-link></p>
      </form>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        username: '',
        password: ''
      }
    },
    methods: {
      // В LoginView.vue
async handleLogin() {
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
  }
  
  button:hover {
    background-color: #369f6b;
  }
  </style>