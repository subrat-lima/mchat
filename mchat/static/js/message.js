import { getToken, deleteToken, domElem, domText, domSet } from "./helper.js";
import Home from "./home.js";

export class Message {
  constructor(id, type) {
    this.ui(id, type);
  }

  async ui(id, type) {
    let messages = await this.apiGetMessages(id, type);
    console.log("messages: ", messages);
    if (!messages) {
      return;
    }
    let ul = domElem("ul");
    for (let message of messages) {
      let li = domElem("li", {
        "data-id": message["id"],
        "data-sender-id": message["sender_id"],
      });
      let msg = domElem("p");
      domSet(msg, domText(message["message"]));
      let date = domElem("p");
      domSet(date, domText(message["create_date"]));
      let sender = domElem("p");
      domSet(sender, domText(message["sender_name"]));
      domSet(li, [msg, date, sender]);
      domSet(ul, li, false);
    }

    domSet(null, [ul]);
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
      let messages = await response.json();
      return messages;
    } else if (response.status == 401) {
      deleteToken();
      new Home();
    }
  }
}
