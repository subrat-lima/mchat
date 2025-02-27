import handler from "./handler.js";
import { getToken, sleep } from "./helper.js";

let worker = (async function () {
  if (!getToken()) {
    return {};
  }
  let worker = new SharedWorker("/static/js/worker.js");
  let id = self.crypto.randomUUID();
  let webSocketState = WebSocket.CONNECTING;

  worker.port.start();

  worker.port.onmessage = async (event) => {
    switch (event.data.type) {
      case "WSState":
        webSocketState = event.data.state;
        break;
      case "message":
        let hr = await handler;
        await hr.messageFromPort(event.data);
        break;
    }
  };

  let broadcastChannel = new BroadcastChannel("WebSocketChannel");
  broadcastChannel.addEventListener("message", async (event) => {
    switch (event.data.type) {
      case "WSState":
        webSocketState = event.data.state;
        break;
      case "message":
        let hr = await handler;
        await hr.messageFromBroadcast(event.data);
        break;
    }
  });

  async function postMessageToWSServer(input) {
    if (webSocketState == WebSocket.CONNECTING) {
      console.log("still connecting to the server, try again later!");
    } else if (
      webSocketState == WebSocket.CLOSING ||
      webSocketState == WebSocket.CLOSED
    ) {
      console.log("connection closed!");
    } else {
      worker.port.postMessage({
        from: id,
        ...input,
      });
    }
  }

  let token = getToken();
  await sleep(2000);
  await postMessageToWSServer({ action: "token", token: token });

  return {
    send: postMessageToWSServer,
  };
})();

export default worker;
