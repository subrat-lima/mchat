import { getUser, getToken, showToast } from "./helper.js";

export default class Socket {
  constructor() {
    let username = getUser();
    this.socket = new WebSocket(`/ws/${username}`);

    this.socket.onopen = this.openHandler;
    this.socket.onmessage = this.messageHandler;
    this.socket.onclose = this.closeHandler;
  }

  openHandler(e) {
    showToast("socket connected");
  }

  messageHandler(e) {
    console.log("e: ", e);
    try {
      let data = JSON.parse(e.data);
      console.log("data: ", data);
    } catch (e) {
      console.log("error: ", e);
    }
  }

  closeHandler(e) {
    showToast("socket closed");
  }

  sendMessage(message) {
    message = { hello: "world" };
    this.socket.send(JSON.stringify(message));
    showToast("socket send message");
  }

  send(message) {
    message["token"] = getToken();
    this.socket.send(JSON.stringify(message));
  }
}
