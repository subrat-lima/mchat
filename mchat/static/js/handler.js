import dom from "./dom.js";
import ui from "./ui.js";
import db from "./db.js";
import { sleep, get, set, del } from "./helper.js";
import worker from "./main.worker.js";

let handler = (function () {
  async function httpAuth(e) {
    e.preventDefault();
    let form = e.target;
    let url = form.getAttribute("action");
    let attrs = {
      method: "post",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({
        username: form.username.value,
        password: form.password.value,
      }),
    };
    let response = await fetch(url, attrs).then((resp) => resp.json());
    return response;
  }

  async function loadAuth(e) {
    e.preventDefault();
    ui.auth(e.target.getAttribute("href"));
  }

  async function serverAuth(e) {
    let response = await httpAuth(e);
    let message = await response.detail;
    let m_type = (await response.status) ? "info" : "error";
    let path = e.target.id;
    ui.showToast(message, m_type);
    if (!response.status) {
      return;
    }
    if (path == "register") {
      return ui.auth("login");
    }
    let token = await response.access_token;
    set("token", token);
    init();
  }

  function init() {
    if (!get("token")) {
      return ui.auth("login");
    }
    loadRooms();
    syncServer();
  }

  /* refactored end  */

  //let last_synced = db.last_synced();
  //let wr = await worker;
  //await wr.send({ action: "sync", from: last_synced });
  //await wr.send({ action: "get-contacts" });
  //await wr.send({ action: "get-chat-list" });

  function loadRooms() {
    ui.loader();
    ui.rooms([]);
    ui.loader(false);
  }

  function syncServer() {}

  function view(name) {
    if (name == "addChat") {
      ui.addChat();
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

  async function messageFromBroadcast(data) {
    messageFromPort(data);
  }

  async function messageFromPort(j_data) {
    let data = j_data["data"];
    let action = data["action"];
    if (action == "get-chat-list") {
      ui.rooms(data["chats"]);
    } else if (action == "open-chat") {
      ui.messageList(data["chat"], data["messages"]);
    } else if (action == "send-message") {
      wsSendMessageResponse(j_data);
    } else if (action == "token") {
      await wsTokenResponse(data);
    } else if (action == "add-chat") {
      if (data["status"] == "ok") {
        await wsOpenChat(data["chat"], data["messages"]);
      } else {
        document.getElementById("dialog").remove();
        ui.showToast(data["error"], "error");
      }
    } else if (action == "get-contacts") {
      let contacts = data["contacts"];
      console.log("contacts: ", contacts);
      //db.addUsers(contacts);
    }
  }

  async function wsSendMessageResponse(j_data) {
    console.log("j_data: ", j_data);
    let current_ui = document.querySelector("main > div");
    let ui_id = current_ui.id;
    let receiver_id = current_ui.dataset.receiver_id;
    if (ui_id == "main-chat") {
      ui.messageAdd(data["message"]);
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
    loadRooms();
  }

  function logout(e) {
    e.preventDefault();
    del(["token", "username", "id"]);
    location.reload();
    ui.showToast("logout successful");
  }

  return {
    init: init,
    loadAuth: loadAuth,
    serverAuth: serverAuth,
    /* refactored end */
    view: view,
    messageFromBroadcast: messageFromBroadcast,
    messageFromPort: messageFromPort,
    apiSendMessage: apiSendMessage,
    apiAddChat: apiAddChat,
    loadAddChat: loadAddChat,
    loadChat: loadChat,
    apiOpenChat: apiOpenChat,
    logout: logout,
  };
})();

export default handler;
