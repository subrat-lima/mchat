//import dom from "./dom.js";
//import ui from "./ui.js";
//import worker from "./main.worker.js";
import handler from "./handler.js";

async function init(e) {
  handler.init();
}

document.addEventListener("DOMContentLoaded", init);
