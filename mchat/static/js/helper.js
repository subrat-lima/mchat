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

export function domElem(name, attrs = {}, eventListeners = {}) {
  let elem = document.createElement(name);
  for (let [key, value] of Object.entries(attrs)) {
    elem.setAttribute(key, value);
  }
  for (let [key, value] of Object.entries(eventListeners)) {
    elem.addEventListener(key, value);
  }
  return elem;
}

export function domText(name) {
  return document.createTextNode(name);
}

export function domSet(parent, children = []) {
  parent.innerHTML = "";
  for (let child of [...children]) {
    parent.appendChild(child);
  }
}
