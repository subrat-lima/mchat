import Home from "./home.js";
import Contact from "./contact.js";
import { Chat } from "./chat.js";
import { getToken, deleteToken } from "./helper.js";

async function init() {
  let token = getToken();
  if (token) {
    new Chat();
    console.log("chat view");
  } else {
    console.log("home view");
    new Home();
  }
}

document.addEventListener("DOMContentLoaded", init);
