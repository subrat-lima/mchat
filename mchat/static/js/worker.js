let ws = new WebSocket("/ws");

let broadcastChannel = new BroadcastChannel("WebSocketChannel");

const idToPortMap = {};

ws.onopen = () =>
  broadcastChannel.postMessage({ type: "WSState", state: ws.readyState });
ws.onclose = () =>
  broadcastChannel.postMessage({ type: "WSState", state: ws.readyState });

ws.onmessage = ({ data }) => {
  console.log(data);
  let parsedData = { data: JSON.parse(data), type: "message" };
  if (!parsedData.data.from) {
    broadcastChannel.postMessage(parsedData);
  } else {
    idToPortMap[parsedData.data.from].postMessage(parsedData);
  }
};

onconnect = (e) => {
  let port = e.ports[0];
  port.onmessage = (msg) => {
    idToPortMap[msg.data.from] = port;
    console.log("data: ", msg.data);
    ws.send(JSON.stringify({ data: msg.data }));
  };
  port.postMessage({ state: ws.readyState, type: "WSState" });
};
