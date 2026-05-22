

const BASE_URL = "https://nexivo-kzn8.onrender.com"; 


function getUserId() {
  return localStorage.getItem("user_id");
}

function getUserName() {
  return localStorage.getItem("user_name");
}

function isLoggedIn() {
  return !!getUserId();
}

function logout() {
  localStorage.removeItem("user_id");
  localStorage.removeItem("user_name");
  window.location.href = "index.html";
}

// ---- USER API ----
async function signup(name, email, password) {
  const res = await fetch(`${BASE_URL}/users/signup`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name, email, password })
  });
  return res.json();
}

async function login(email, password) {
  const res = await fetch(`${BASE_URL}/users/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password })
  });
  return res.json();
}

// ---- APPLICATION API ----
async function getApplications() {
  const res = await fetch(`${BASE_URL}/applications/user/${getUserId()}`);
  return res.json();
}

async function createApplication(data) {
  const res = await fetch(`${BASE_URL}/applications/${getUserId()}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  });
  return res.json();
}

async function updateApplication(appId, data) {
  const res = await fetch(`${BASE_URL}/applications/${appId}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  });
  return res.json();
}

async function deleteApplication(appId) {
  const res = await fetch(`${BASE_URL}/applications/${appId}`, {
    method: "DELETE"
  });
  return res.json();
}

// ---- INTERVIEW ROUNDS API ----
async function getRounds(appId) {
  const res = await fetch(`${BASE_URL}/rounds/${appId}`);
  return res.json();
}

async function createRound(appId, data) {
  const res = await fetch(`${BASE_URL}/rounds/${appId}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  });
  return res.json();
}

async function deleteRound(roundId) {
  const res = await fetch(`${BASE_URL}/rounds/delete/${roundId}`, {
    method: "DELETE"
  });
  return res.json();
}

// ---- DASHBOARD API ----
async function getDashboardStats() {
  const res = await fetch(`${BASE_URL}/dashboard/${getUserId()}`);
  return res.json();
}

async function getWeaknesses() {
  const res = await fetch(`${BASE_URL}/dashboard/weaknesses/${getUserId()}`);
  return res.json();
}

// ---- HELPERS ----
function formatDate(dateStr) {
  if (!dateStr) return "-";
  return new Date(dateStr).toLocaleDateString("en-IN", {
    day: "2-digit", month: "short", year: "numeric"
  });
}

function getStatusBadge(status) {
  const map = {
    "Applied": "badge-applied",
    "Interview Scheduled": "badge-scheduled",
    "Rejected": "badge-rejected",
    "Selected/Offer": "badge-selected"
  };
  return `<span class="badge ${map[status] || ''}">${status}</span>`;
}

function getResultBadge(result) {
  const map = {
    "Passed": "badge-passed",
    "Failed": "badge-failed",
    "Pending": "badge-pending",
    "On Hold": "badge-hold"
  };
  return `<span class="badge ${map[result] || ''}">${result}</span>`;
}

function showAlert(elementId, message, type = "error") {
  const el = document.getElementById(elementId);
  if (!el) return;
  el.textContent = message;
  el.className = `alert alert-${type} show`;
  setTimeout(() => el.classList.remove("show"), 4000);
}
