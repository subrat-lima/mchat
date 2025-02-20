import Home from "./home.js";
import { getToken, deleteToken } from "./helper.js";

async function init() {
  let token = getToken();
  if (token) {
    console.log("chat view");
  } else {
    console.log("home view");
    new Home();
  }
}

document.addEventListener("DOMContentLoaded", init);
