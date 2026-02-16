// Import the functions you need from the SDKs you need
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-app.js";
import { getFirestore } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore.js";
import { getAuth } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-auth.js";
import { getStorage } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-storage.js";

// TODO: Replace the following with your app's Firebase project configuration
// See: https://firebase.google.com/docs/web/learn-more#config-object
const firebaseConfig = {
  apiKey: "AIzaSyB6J2dVCoKPdlXTYS-bhSkZNyTtY0Xzj9M",
  authDomain: "bankschool-f3813.firebaseapp.com",
  projectId: "bankschool-f3813",
  storageBucket: "bankschool-f3813.firebasestorage.app",
  messagingSenderId: "651157753991",
  appId: "1:651157753991:web:5c86d8b4e2a68d3de76822"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const db = getFirestore(app);
const auth = getAuth(app);
const storage = getStorage(app);

export { db, auth, storage };
