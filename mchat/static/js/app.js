import Home from "./home.js";
import { Chat } from "./chat.js";
import Socket from "./socket.js";
import { sleep, getUser, getToken, deleteToken, showToast } from "./helper.js";

async function init() {
  let token = getToken();
  let socket = new Socket();
  console.log("socket: ", socket);
  if (token) {
    console.log("socket: ", socket);
    new Chat(socket);
    console.log("chat view");
  } else {
    console.log("home view");
    console.log("socket: ", socket);
    new Home(socket);
  }
}

document.addEventListener("DOMContentLoaded", init);

//let user = getUser();
//let token = getToken();
//let ws = new WebSocket(`/ws/${user}`);
//
//ws.addEventListener("open", (e) => {
//  ws.onmessage = function (event) {
//    showToast(event.data);
//    console.log("onmessage.data: ", event.data);
//  };
//
//  function sendMessage() {
//    ws.send("hello world");
//    console.log("send data");
//  }
//
//  sleep(5000);
//  sendMessage();
//});
