<template>
  <div id="app">
    <h1>Google Login with Firebase</h1>
    <button @click="loginWithGoogle">Login with Google</button>
    <div v-if="user">
      <h2>Welcome, {{ user.displayName }}</h2>
      <img :src="user.photoURL" alt="Profile Picture" />
    </div>
  </div>
</template>

<script>
import { auth, provider } from "./firebase"; // Import from firebase.js
import { signInWithPopup } from "firebase/auth";

export default {
  data() {
    return {
      user: null,
    };
  },
  methods: {
    async loginWithGoogle() {
      try {
        const result = await signInWithPopup(auth, provider);

        // Get the user info
        const user = result.user;
        this.user = user;

        // Get ID token from Firebase Authentication
        const idToken = await user.getIdToken();
        console.log("ID Token:", idToken);

        // Send ID Token to the Django backend
        await this.sendIdTokenToBackend(idToken);
      } catch (error) {
        console.error("Login error:", error);
      }
    },
    async sendIdTokenToBackend(idToken) {
      try {
        const response = await fetch("http://localhost:8000/api/verify-id-token/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ idToken }),
        });

        const data = await response.json();
        console.log("Backend response:", data);

        if (data.success) {
          // You can access user details here
          this.userDetails = data.user;
        }
      } catch (error) {
        console.error("Error sending token to backend:", error);
      }
    } 
  },
};
</script>

<style>
h1 {
  font-family: Arial, sans-serif;
}
</style>
