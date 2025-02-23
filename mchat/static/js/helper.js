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

export function domSet(parent = null, children = [], clean = true) {
  if (!parent) {
    parent = document.querySelector("main");
  }
  if (clean) {
    parent.innerHTML = "";
  }
  if (!Array.isArray(children)) {
    children = [children];
  }
  for (let child of children) {
    parent.appendChild(child);
  }
}

export function showToast(msg, category = "info") {
  var x = document.getElementById("toast");
  domSet(x, domText(msg));

  x.classList.add("show");
  x.classList.add(category);

  setTimeout(() => {
    x.classList.remove("show");
    x.classList.remove(category);
  }, 3000);
}
