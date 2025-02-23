import { getToken, deleteToken, domElem, domText, domSet } from "./helper.js";
import Home from "./home.js";
import { Message } from "./message.js";

export class Chat {
  constructor() {
    this.uiShow();
  }

  async uiShow() {
    let chats = await this.apiGetChats();
    console.log("chats: ", chats);
    if (!chats) {
      return;
    }
    let button = domElem(
      "button",
      { class: "container" },
      { click: this.uiAddChat },
    );
    domSet(button, domText("add chat"));

    let ul = domElem("ul");
    for (let chat of chats) {
      let chat_id = chat["recipient_id"];
      let chat_type = "direct";
      if (!chat_id) {
        chat_id = chat["recipient_group_id"];
        chat_type = "group";
      }
      let li = domElem(
        "li",
        {
          "data-id": chat_id,
          "data-type": chat_type,
        },
        { click: this.showMessages },
      );
      let a = domElem("a");
      domSet(li, domText(chat["name"]));
      domSet(ul, li, false);
    }

    domSet(null, [button, ul]);
  }

  uiAddChat() {
    new AddChat();
  }

  showMessages(e) {
    let elem = e.target;
    let chat_id = elem.getAttribute("data-id");
    let chat_type = elem.getAttribute("data-type");
    new Message(chat_id, chat_type);
  }

  async apiGetChats() {
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
