// ============================================
//  BOND CENTRAL — Main JavaScript
// ============================================

// --- Mobile Menu ---
function toggleMenu() {
  const nav = document.querySelector('.nav-links');
  nav.classList.toggle('open');
}

// ============================================
//  GLOBAL DATA
// ============================================
let BONDS_DATA = [];


const API_URL = "https://bondcentral-backend.onrender.com";

// ============================================
//  FETCH DATA FROM BACKEND
// ============================================

function loadBonds() {
  fetch(`${API_URL}/api/bonds`)   
    .then(res => res.json())
    .then(data => {
      console.log("API Response:", data);

      BONDS_DATA = data.bonds;
      window.BONDS_DATA = BONDS_DATA;

      displayBonds(BONDS_DATA);
    })
    .catch(err => {
      console.error("Error fetching bonds:", err);
      alert("Backend not connected ❌");
    });
}