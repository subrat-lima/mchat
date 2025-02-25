import { getToken, deleteToken, domElem, domText, domSet } from "./helper.js";
import Home from "./home.js";
import { Message } from "./message.js";

export class Chat {
  constructor(socket) {
    this.socket = socket;
    this.uiShow();
    console.log("socket: ", socket);
    console.log("this.socket: ", this.socket);
  }

  async uiShow() {
    console.log("this.socket: ", this.socket);
    let chats = await this.apiGetChats();
    if (!chats) {
      return;
    }
    let button = domElem(
      "button",
      { class: "container" },
      {
        click: () => {
          this.uiAddChat();
        },
      },
    );
    domSet(button, domText("add chat"));

    let section = domElem("section");
    for (let chat of chats) {
      let chat_id = chat["recipient_id"];
      let chat_type = "direct";
      if (!chat_id) {
        chat_id = chat["recipient_group_id"];
        chat_type = "group";
      }
      let article = domElem(
        "article",
        {
          "data-id": chat_id,
          "data-type": chat_type,
          "data-name": chat["name"],
        },
        {
          click: (e) => {
            this.showMessages(e);
          },
        },
      );
      let a = domElem("a");
      domSet(article, domText(chat["name"]));
      domSet(section, article, false);
    }

    domSet(null, [button, section]);
  }

  uiAddChat() {
    console.log("this.socket: ", this.socket);
    new AddChat(this.socket);
  }

  showMessages(e) {
    let elem = e.target;
    let chat_id = elem.getAttribute("data-id");
    let chat_type = elem.getAttribute("data-type");
    let chat_name = elem.getAttribute("data-name");
    console.log("this.socket: ", this.socket);
    new Message(chat_id, chat_type, chat_name, this.socket);
  }

  async apiGetChats() {
    console.log("this.socket: ", this.socket);
    let token = getToken();
    let response = await fetch("/chats/", {
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    });
    if (response.status == 200) {
      let chats = await response.json();
      return chats;
    } else if (response.status == 401) {
      deleteToken();
      new Home();
    }
  }
}

export class AddChat {
  constructor() {
    this.uiShow();
  }

  async uiShow() {
    // TODO: add this view
    let p = domElem("p");
    domSet(p, domText("page to be build"));
  }
}
