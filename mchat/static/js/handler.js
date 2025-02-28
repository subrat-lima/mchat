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
    let response = await api.auth(e);
    let token = await response.access_token;
    if (token) {
      ui.showToast("login successful", "info");
      set("token", token);
      location.reload();
    } else {
      ui.showToast(response.detail, "error");
    }
  }

  async function apiRegister(e) {
    let response = await api.auth(e);
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
    let form = e.target;
    ui.loader("messages");
    let receiver_id = form.dataset.id;
    let receiver_name = form.dataset.name;
    let wr = await worker;
    await wr.send({
      action: "open-chat",
      receiver_id: receiver_id,
      receiver_name: receiver_name,
    });
  }

  async function wsChatList() {
    let wr = await worker;
    await wr.send({ action: "get-chat-list" });
  }

  async function messageFromBroadcast(data) {
    messageFromPort(data);
  }

  async function messageFromPort(j_data) {
    let data = j_data["data"];
    let action = data["action"];
    if (action == "get-chat-list") {
      ui.chatList(data["chats"]);
    } else if (action == "open-chat") {
      ui.messageList(data["chat"], data["messages"]);
    } else if (action == "send-message") {
      ui.messageAdd(data["message"]);
    } else if (action == "token") {
      await wsTokenResponse(data);
    } else if (action == "add-chat") {
      if (data["status"] == "ok") {
        await wsOpenChat(data["chat"], data["messages"]);
      } else {
        document.getElementById("dialog").remove();
        ui.showToast(data["error"], "error");
      }
    }
  }

  async function wsOpenChat(chat, messages) {
    if (!messages) {
      messages = [];
    }
    ui.messageList(chat, messages);
  }

  async function wsTokenResponse(resp) {
    if (resp["status"] == "failed") {
      del(["token", "username", "id"]);
      view("login");
    } else {
      let { username, id } = resp["user"];
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
      message: {
        data: form.data.value,
        receiver_id: form.dataset.id,
        message_type: form.message_type.value,
        parent_message_id: form.parent_message_id.value,
        expiry_date: null,
      },
    });
    form.data.value = "";
    form.message_type.value = "";
    form.parent_message_id.value = "";
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
    view("addChat");
  }

  async function apiAddChat(e) {
    e.preventDefault();
    let username = e.target.username.value;
    let wr = await worker;
    await wr.send({ action: "add-chat", username: username });
  }

  async function loadChat(e) {
    e.preventDefault();
    view("chatList");
  }

  function logout(e) {
    e.preventDefault();
    del(["token", "username", "id"]);
    location.reload();
    ui.showToast("logout successful");
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
