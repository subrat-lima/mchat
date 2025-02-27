import dom from "./dom.js";
import ui from "./ui.js";
import api from "./api.js";
import { sleep, get, set, del } from "./helper.js";
import worker from "./main.worker.js";

let handler = (function () {
  function view(name) {
    if (name == "login") {
      ui.login(handler);
    } else if (name == "register") {
      ui.register(handler);
    } else if (name == "chatList") {
      ui.loader("chat");
      wsChatList();
    } else if (name == "addChat") {
      ui.addChat();
    }
  }

  async function loadLogin(e) {
    e.preventDefault();
    view("login");
  }

  async function loadRegister(e) {
    e.preventDefault();
    view("register");
  }

  async function apiLogin(e) {
    e.preventDefault();
    let form = e.target;
    let response = await api.login(form.username.value, form.password.value);
    let token = await response.access_token;
    console.log("token: ", token);
    if (token) {
      ui.showToast("login successful", "info");
      set("token", token);
      location.reload();
    } else {
      ui.showToast(response.detail, "error");
    }
  }

  async function apiRegister(e) {
    e.preventDefault();
    let form = e.target;
    let response = await api.register(form.username.value, form.password.value);
    let error = response.detail;
    let message = response.message;
    if (message) {
      ui.showToast(message, "info");
      view("login");
    } else {
      ui.showToast(error, "error");
    }
  }

  async function apiOpenChat(e) {
    e.preventDefault();
    console.log("open chat");
    ui.loader("messages");
    let article = e.target;
    let receiver_id = article.dataset.id;
    let type = article.dataset.type;
    let name = article.dataset.name;
    let wr = await worker;
    await wr.send({
      action: "open-chat",
      receiver_id: receiver_id,
      type: type,
    });
  }

  async function wsChatList() {
    let wr = await worker;
    await wr.send({ action: "get-chat-list" });
  }

  async function messageFromBroadcast(data) {
    console.log("msg for everyone");
    console.log(data);
    messageFromPort(data);
  }

  async function messageFromPort(j_data) {
    let data = j_data["data"];
    let action = data["action"];
    if (action == "get-chat-list") {
      ui.chatList(data["data"], handler);
    } else if (action == "open-chat") {
      ui.messageList(data["chat"], data["data"]);
    } else if (action == "send-message") {
      console.log("in send-message");
      console.log(data);
      ui.messageAdd(data["data"], data["current_user"]);
    } else if (action == "token") {
      await wsTokenResponse(data);
    } else if (action == "add-chat") {
      await wsOpenChat(data["data"]);
    }
  }

  async function wsOpenChat(chat, messages = []) {
    console.log("chat: ", chat);
    ui.messageList(chat, messages);
  }

  async function wsTokenResponse(resp) {
    if (resp["status"] == "failed") {
      del(["token", "username", "id"]);
      view("login");
    } else {
      let { username, id } = resp["data"];
      set("username", username);
      set("id", id);
    }
  }

  async function apiSendMessage(e) {
    e.preventDefault();
    let form = e.target;
    let wr = await worker;
    await wr.send({
      action: "send-message",
      message: form.message.value,
      receiver_id: form.dataset.id,
      type: form.dataset.type,
      parent_id: form.parent_id.value,
    });
    form.message.value = "";
  }

  function backToChatView(e) {
    e.preventDefault();
    view("chatList");
  }

  function init() {
    let token = get("token");
    if (token) {
      view("chatList");
    } else {
      view("login");
    }
  }

  function loadAddChat(e) {
    e.preventDefault();
    console.log("load chat");
    view("addChat");
  }

  async function apiAddChat(e) {
    e.preventDefault();
    let username = e.target.username.value;
    let wr = await worker;
    await wr.send({ action: "add-chat", data: { username: username } });

    console.log("api add chat");
  }

  async function loadChat(e) {
    e.preventDefault();
    view("chatList");
  }

  function logout(e) {
    e.preventDefault();
    del(["token", "username", "id"]);
    location.reload();
    console.log("logout successful");
    ui.showToast("logout successfully");
  }

  return {
    view: view,
    init: init,
    messageFromBroadcast: messageFromBroadcast,
    messageFromPort: messageFromPort,
    loadRegister: loadRegister,
    loadLogin: loadLogin,
    apiLogin: apiLogin,
    apiSendMessage: apiSendMessage,
    apiRegister: apiRegister,
    apiAddChat: apiAddChat,
    loadAddChat: loadAddChat,
    loadChat: loadChat,
    apiOpenChat: apiOpenChat,
    logout: logout,
  };
})();

export default handler;
