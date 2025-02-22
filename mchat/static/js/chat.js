import { getToken, domElem, domText, domSet } from "./helper.js";

export default class Chat {
  constructor() {
    this.uiShow();
  }

  async uiShow() {
    let chats = await this.apiGetChats();
    console.log("chats: ", chats);
    let main = document.querySelector("main");
    let button = domElem("button", {}, { click: this.uiAddChat });
    domSet(button, domText("add chat"));

    let ul = domElem("ul");
    for (let chat of chats) {
      let li = domElem("li", {
        "data-recipient-id": chat["recipient_id"],
        "data-recipient-group-id": chat["recipient_group_id"],
      });
      domSet(li, domText(chat["name"]));
      domSet(ul, li, false);
    }

    domSet(main, [button, ul]);
  }

  uiAddChat() {}

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
    }
  }
}
