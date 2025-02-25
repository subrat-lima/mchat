import {
  getToken,
  getDisplayDate,
  deleteToken,
  domElem,
  domText,
  domSet,
  getUser,
  showToast,
} from "./helper.js";
import Home from "./home.js";
import { Chat } from "./chat.js";

export class Message {
  constructor(id, type, chat_name, socket) {
    this.socket = socket;
    this.ui(id, type, chat_name);
    console.log("this.socket: ", this.socket);
  }

  uiAddMessage(message, section = null) {
    let user = getUser();
    if (!section) {
      section = document.getElementById("message-div");
    }

    let article = domElem("article", {
      "data-id": message["id"],
      "data-sender-id": message["sender_id"],
    });
    let is_me = user == message["sender_name"];
    article.classList.add("message");
    if (is_me) {
      article.classList.add("right");
    } else {
      article.classList.add("left");
    }
    let msg = domElem("span");
    domSet(msg, domText(message["message"]));
    msg.classList.add("text");
    let date = domElem("small");
    date.classList.add("date");
    date.classList.add("right");
    domSet(date, domText(getDisplayDate(message["create_date"])));
    domSet(article, [msg, date]);
    domSet(section, article, false);
  }

  async ui(id, type, chat_name) {
    console.log("this.socket: ", this.socket);
    let user = getUser();
    let messages = await this.apiGetMessages(id, type);
    console.log("messages: ", messages);
    if (!messages) {
      return;
    }
    let section = domElem("section", { id: "message-div" });
    for (let message of messages) {
      this.uiAddMessage(message, section);
    }

    let form = domElem(
      "form",
      { "data-id": id, "data-type": type, "data-name": chat_name },
      {
        submit: (e) => {
          this.apiSendMessage(e);
        },
      },
    );
    let fieldset = domElem("fieldset", { role: "group" });
    let text = domElem("input", {
      type: "text",
      name: "message",
      placeholder: "message",
    });
    let submit = domElem("input", { type: "submit", value: "send" });
    domSet(fieldset, [text, submit]);
    domSet(form, fieldset);

    let header = domElem("article");
    let back_button = domElem(
      "span",
      {},
      {
        click: () => {
          this.goBack();
        },
      },
    );
    back_button.classList.add("back-btn");
    back_button.innerHTML = "&#8592;";
    let header_text = domElem("strong");
    domSet(header_text, domText(chat_name));

    //header.classList.add("chat-head");
    domSet(header, [back_button, header_text]);
    domSet(null, [header, section, form]);
  }

  async goBack() {
    new Chat(this.socket);
  }

  async apiSendMessage(e) {
    e.preventDefault();
    let token = getToken();
    let elem = e.target;
    let chat_id = elem.getAttribute("data-id");
    let chat_type = elem.getAttribute("data-type");
    let chat_name = elem.getAttribute("data-name");
    let message = {
      type: "send_message",
      temp_id: "temp-" + new Date().getTime(),
      message: elem.message.value,
      category: 0,
      parent_message_id: null,
      recipient_id: chat_id,
      recipient_group_id: null,
    };
    this.socket.send(message);
    this.uiAddMessage({
      id: message["temp_id"],
      sender_id: -1,
      sender_name: getUser(),
      message: message["message"],
      create_date: new Date(),
    });
    //let response = await fetch(`/chats/messages/`, {
    //  method: "POST",
    //  body: JSON.stringify(message),
    //  headers: {
    //    "Content-Type": "application/json",
    //    Authorization: `Bearer ${token}`,
    //  },
    //});
    //if (response.status == 200) {
    //  showToast("message sent");
    //  console.log("this.socket: ", this.socket);
    //  this.socket.sendMessage(message["message"]);
    //  new Message(chat_id, chat_type, chat_name, this.socket);
    //} else if (response.status == 401) {
    //  response = await response.json();
    //  showToast(response.detail, "error");
    //}
  }

  async apiGetMessages(id, type) {
    let token = getToken();
    let response = await fetch(`/chats/messages/${type}/${id}`, {
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    });
    if (response.status == 200) {
      console.log("this.socket: ", this.socket);
      let messages = await response.json();
      return messages;
    } else if (response.status == 401) {
      deleteToken();
      new Home(this.socket);
    }
  }
}
