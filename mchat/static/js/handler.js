import dom from "./dom.js";
import ui from "./ui.js";
import api from "./api.js";
import { sleep, getToken, setToken } from "./helper.js";
import worker from "./main.worker.js";

let handler = (function () {
  function view(name) {
    if (name == "home") {
      ui.home(openLogin, openRegister);
    } else if (name == "login") {
      ui.auth("login", apiLogin);
    } else if (name == "register") {
      ui.auth("register", apiRegister);
    } else if (name == "chatList") {
      ui.loader("chat");
      wsChatList();
    }
  }

  async function openLogin(e) {
    e.preventDefault();
    view("login");
  }

  async function openRegister(e) {
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
      setToken(token);
      view("chatList");
    } else {
      ui.showToast(response.detail, "error");
    }
  }

  async function apiRegister(e) {
    e.preventDefault();
    let form = e.target;
    let response = await api.register(form.username.value, form.password.value);
    let error = response.detail;
    if (error) {
      ui.showToast(error, "error");
    } else {
      ui.showToast("register successful", "info");
      view("home");
    }
  }

  async function apiOpenChat(e) {
    e.preventDefault();
    ui.loader("messages");
    let article = e.target;
    let receiver_id = article.dataset.id;
    let type = article.dataset.type;
    let name = article.dataset.name;
    // TODO: add remaining info for chat
    await sleep(1000);
    console.log("worker: ", await worker);
    let wr = await worker;
    await wr.send({
      action: "open-chat",
      receiver_id: receiver_id,
      type: type,
    });
  }

  async function wsChatList() {
    let wr = await worker;
    console.log("worker: ", await worker);
    console.log("send: ", await worker.send);
    console.log("wr send: ", await wr.send);

    await wr.send({ action: "get-chat-list" });
  }

  async function messageFromBroadcast(data) {
    console.log("msg for everyone");
    console.log(data);
    messageFromPort(data);
  }

  async function messageFromPort(j_data) {
    console.log(`msg for user with id`);
    console.log(j_data);
    let data = j_data["data"];
    let action = data["action"];
    if (action == "get-chat-list") {
      console.log("actioned");
      ui.chatList(data["data"], apiOpenChat);
    } else if (action == "open-chat") {
      ui.messageList(
        data["data"],
        data["chat"],
        apiSendMessage,
        backToChatView,
      );
    } else if (action == "send-message") {
      console.log("in send-message");
      console.log(data);
      ui.messageAdd(data["data"], data["current_user"]);
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
    let token = getToken();
    if (token) {
      view("chatList");
    } else {
      view("home");
    }
  }

  return {
    view: view,
    init: init,
    messageFromBroadcast: messageFromBroadcast,
    messageFromPort: messageFromPort,
    //login: login,
    //register: register,
    //openChat: openChat,
  };
})();

export default handler;
