import dom from "./dom.js";
import { getDisplayDate, get } from "./helper.js";
import handler from "./handler.js";

let ui = (function () {
  function register() {
    let section = dom.elem("section", { cls: "auth" });
    let header = dom.elem("div", { cls: "header" });
    let logo = dom.elem("img", { cls: "logo", src: "/static/img/chat.png" });
    let header_text = dom.elem("strong");

    let article = dom.elem("article");
    let inputs = [{ name: "username" }, { name: "password", type: "password" }];
    let form = dom.form("register", inputs, handler.apiRegister);

    let footer = dom.elem("footer", { cls: "footer" });
    let footer_text = dom.elem("p");
    let a = dom.link("#login", "login", handler.loadLogin);

    dom.set(header_text, dom.text("mchat"));
    dom.set(header, [logo, header_text]);
    dom.set(article, form);
    dom.set(footer_text, [dom.text("Already have an account ? "), a]);
    dom.set(footer, footer_text);
    dom.set(section, [header, article, footer]);
    dom.set(null, section);
  }

  function login() {
    let section = dom.elem("section", { cls: "auth" });
    let header = dom.elem("div", { cls: "header" });
    let logo = dom.elem("img", { cls: "logo", src: "/static/img/chat.png" });
    let header_text = dom.elem("strong");

    let article = dom.elem("article");
    let inputs = [{ name: "username" }, { name: "password", type: "password" }];
    let form = dom.form("login", inputs, handler.apiLogin);

    let footer = dom.elem("footer", { cls: "footer" });
    let footer_text = dom.elem("p");
    let a = dom.link("#register", "register now", handler.loadRegister);

    dom.set(header_text, dom.text("mchat"));
    dom.set(header, [logo, header_text]);
    dom.set(article, form);
    dom.set(footer_text, [dom.text("Don't have an account ? "), a]);
    dom.set(footer, footer_text);
    dom.set(section, [header, article, footer]);
    dom.set(null, section);
  }

  function addChat() {
    console.log("inside addchat");
    let dialog = dom.elem("dialog", { open: true });
    let article = dom.elem("article");
    let header = dom.elem("p");
    let button = dom.elem(
      "button",
      { "aria-label": "Close", rel: "prev", cls: "close" },
      {
        click: (e) => {
          dialog.remove();
        },
      },
    );

    let inputs = [{ name: "username" }];
    let form = dom.form("new chat", inputs, handler.apiAddChat);

    dom.set(header, button);
    dom.set(article, [header, form]);
    dom.set(dialog, article);
    dom.set(null, dialog, false);
  }

  function chatList(chats) {
    let section = dom.elem("section", { cls: "chat" });
    let article = dom.elem("article", { cls: "header" });
    let header = dom.elem("div");
    let logo = dom.elem("img", { cls: "logo", src: "/static/img/chat.png" });
    let header_text = dom.elem("strong");
    let button_div = dom.elem("div");
    let button_1 = dom.elem("button", {}, { click: handler.loadAddChat });
    let button_2 = dom.elem(
      "button",
      { cls: "secondary" },
      { click: handler.logout },
    );
    let chat_div = dom.elem("div", { cls: "list" });
    dom.set(button_1, dom.text("add"));
    dom.set(button_2, dom.text("logout"));
    dom.set(header_text, dom.text("mchat"));
    dom.set(header, [logo, header_text]);
    dom.set(button_div, [button_1, button_2]);
    dom.set(article, [header, button_div]);
    dom.set(section, [article, chat_div]);

    for (let chat of chats) {
      console.log("chat: ", chat);
      let receiver_id = chat["recipient_id"];
      let type = "direct";
      let name = chat["name"];
      if (!receiver_id) {
        receiver_id = chat["recipient_group_id"];
        type = "group";
      }

      let article = dom.elem(
        "article",
        {
          "data-id": receiver_id,
          "data-type": type,
          "data-name": name,
          cls: "pointer",
        },
        { click: handler.apiOpenChat },
      );
      dom.set(article, dom.text(name));
      dom.set(chat_div, article, false);
    }
    dom.set(null, section);
  }

  function messageAdd(msg) {
    //let { id, sender_id, sender_name, data, type, create_date } = msg;
    let current_user = get("username");
    let { id, sender_id, parent_id, sender_name, message, type, create_date } =
      msg;
    let section = document.getElementById("messages");
    let cls = current_user == sender_name ? "message right" : "message left";
    let article = dom.elem("article", {
      cls: cls,
      "data-id": id,
      "data-sender-id": sender_id,
      "data-parent-id": parent_id,
    });
    // TODO: handle other data types
    let text = dom.elem("span", { cls: "text" });
    dom.set(text, dom.text(message));
    let date = dom.elem("small", { cls: "date right" });
    dom.set(date, dom.text(getDisplayDate(create_date)));
    dom.set(article, [text, date]);
    dom.set(section, article, false);
    console.log("article: ", article);
    console.log("section: ", section);
    console.log("added message");
  }

  function messageList(chat, messages) {
    let { receiver_id, type, name } = chat;
    let main_div = dom.elem("div", { cls: "main-chat" });
    let nav = dom.elem("article");
    let button = dom.elem(
      "span",
      { cls: "back-btn pointer" },
      { click: handler.loadChat },
    );
    let header = dom.elem("strong");
    let section = dom.elem("section", { id: "messages", cls: "list" });
    let form = dom.elem(
      "form",
      { "data-type": type, "data-id": receiver_id, cls: "search-form" },
      { submit: handler.apiSendMessage },
    );
    let fieldset = dom.elem("fieldset", { role: "group" });
    let input = dom.input("message", "text", null, false);
    let input_hidden = dom.input("parent_id", "text", null, false);
    input_hidden.classList.add("hide");
    let submit = dom.elem("input", { type: "submit", value: "send" });

    button.innerHTML = "&#8592;";
    dom.set(header, dom.text(name));
    dom.set(nav, [button, header]);
    dom.set(fieldset, [input, input_hidden, submit]);
    dom.set(form, fieldset);

    dom.set(main_div, [nav, section, form]);
    dom.set(null, main_div);
    for (let msg of messages) {
      console.log("msg: ", msg);
      messageAdd(msg);
    }
  }

  function loader(name = "page") {
    let span = dom.elem("span", { "aria-busy": true, cls: "loader" });
    dom.set(span, dom.text(`loading ${name}, please wait ...`));
    dom.set(null, span);
  }

  function showToast(msg, category = "info") {
    var x = document.getElementById("toast");
    dom.set(x, dom.text(msg));

    x.classList.add("show");
    x.classList.add(category);

    setTimeout(() => {
      x.classList.remove("show");
      x.classList.remove(category);
    }, 3000);
  }

  return {
    login: login,
    register: register,
    chatList: chatList,
    messageAdd: messageAdd,
    messageList: messageList,
    loader: loader,
    showToast: showToast,
    addChat: addChat,
  };
})();

export default ui;
