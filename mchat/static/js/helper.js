export function getToken() {
  return localStorage.getItem("mchat-token");
}

export function setToken(token) {
  localStorage.setItem("mchat-token", token);
}

export function deleteToken() {
  localStorage.removeItem("mchat-token");
}

export function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}
