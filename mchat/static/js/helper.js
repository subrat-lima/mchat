export function getToken() {
  return localStorage.getItem("mchat-token");
}

export function setToken(token) {
  localStorage.setItem("mchat-token", token);
}

export function deleteToken() {
  localStorage.removeItem("mchat-token");
}

export function getUser() {
  return localStorage.getItem("mchat-user");
}

export function setUser(user) {
  localStorage.setItem("mchat-user", user);
}

export function deleteUser() {
  localStorage.removeItem("mchat-user");
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

export function getDisplayDate(utc_date) {
  let date = new Date(utc_date + " UTC");
  let day = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
  let today = new Date();
  today.setHours(0, 0, 0, 0);
  let past_week = new Date();
  past_week.setDate(today.getDate() - 6);
  let display_date = "";
  if (date.getTime() >= today.getTime()) {
    display_date = `${date.getHours()}:${date.getMinutes()}`;
  } else if (date.getTime() >= past_week.getTime()) {
    display_date = `${day[date.getDay()]} ${date.getHours()}:${date.getMinutes()}`;
  } else {
    display_date = date;
  }
  return display_date;
}
