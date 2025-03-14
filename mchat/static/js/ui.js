import dom from "./dom.js";
import { getDisplayDate, get } from "./helper.js";
import handler from "./handler.js";

let ui = (function () {
  function auth(path) {
    let section = dom.elem("section", { cls: "auth" });
    let header = dom.elem("div", { cls: "header" });
    let logo = dom.elem("img", { cls: "logo", src: "/static/img/chat.png" });
    let header_text = dom.elem("strong");

    let article = dom.elem("article");
    let inputs = [{ name: "username" }, { name: "password", type: "password" }];
    let footer = dom.elem("footer", { cls: "footer" });
    let footer_text = dom.elem("p");
    let form, a;

    if (path == "register") {
      form = dom.form("register", inputs, handler.serverAuth);
      a = dom.link("login", "login", handler.loadAuth);
      dom.set(footer_text, [dom.text("Already have an account ? "), a]);
    } else {
      form = dom.form("login", inputs, handler.serverAuth);
      a = dom.link("register", "register now", handler.loadAuth);
      dom.set(footer_text, [dom.text("Don't have an account ? "), a]);
    }
    dom.set(header_text, dom.text("mchat"));
    dom.set(header, [logo, header_text]);
    dom.set(article, form);
    dom.set(footer, footer_text);
    dom.set(section, [header, article, footer]);
    dom.set(null, section);
  }

  function addChat() {
    let dialog = dom.elem("dialog", { id: "dialog", open: true });
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

  function rooms(chats) {
    let section = dom.elem("section", { cls: "chat" });
    let article = dom.elem("article", { cls: "header" });
    let header = dom.elem("div");
    let logo = dom.elem("img", { cls: "logo", src: "/static/img/chat.png" });
    let header_text = dom.elem("strong");
    let button_div = dom.elem("div");
    let button_1 = dom.elem("button", {}, { click: handler.loadAddChat });
    let button_2 = dom.elem(
      "button",
      { cls: "outline secondary" },
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
      let me = get("username");
      let chat_id = chat["receiver_id"];
      let chat_name = chat["receiver_username"];
      let sender_name = chat["sender_username"];
      if (me == chat_name) {
        chat_id = chat["sender_id"];
        chat_name = chat["sender_username"];
      }

      if (me == sender_name) {
        sender_name = "me";
      }

      let attrs = {
        "data-id": chat_id,
        "data-name": chat_name,
        cls: "pointer",
      };
      let article = dom.elem("article", attrs, { click: handler.apiOpenChat });
      let span = dom.elem("div", attrs);
      let small = dom.elem("small", attrs);

      dom.set(span, dom.text(chat_name));
      dom.set(small, dom.text(`${sender_name}: ${chat["data"]}`));
      dom.set(article, [span, small]);
      dom.set(chat_div, article, false);
    }
    dom.set(null, section);
  }

  function messageAdd(msg) {
    let me = get("username");
    let {
      id,
      sender_username,
      parent_message_id,
      data,
      message_type,
      create_date,
      status,
      expiry_date,
    } = msg;
    let section = document.getElementById("messages");
    let cls = me == sender_username ? "message right" : "message left";
    let article = dom.elem("article", {
      cls: cls,
      "data-id": id,
      "data-parent-id": parent_message_id,
    });
    // TODO: handle other data types
    let text = dom.elem("span", { cls: "text" });
    dom.set(text, dom.text(data));
    let date = dom.elem("small", { cls: "date right" });
    dom.set(date, dom.text(getDisplayDate(create_date)));
    dom.set(article, [text, date]);
    dom.set(section, article, false);
  }

  function messageList(chat, messages) {
    let chat_id = chat["id"];
    let chat_name = chat["name"];
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
      { "data-id": chat_id, cls: "search-form" },
      { submit: handler.apiSendMessage },
    );
    let fieldset = dom.elem("fieldset", { role: "group" });
    let input = dom.input("data", "text", "message", false);
    let input_hidden = dom.input("parent_message_id", "text", null, false);
    let input_hidden_2 = dom.input("message_type", "text", null, false);
    input_hidden.classList.add("hide");
    input_hidden_2.classList.add("hide");
    let submit = dom.elem("input", { type: "submit", value: "send" });

    button.innerHTML = "&#8592;";
    dom.set(header, dom.text(chat_name));
    dom.set(nav, [button, header]);
    dom.set(fieldset, [input, input_hidden, input_hidden_2, submit]);
    dom.set(form, fieldset);

    dom.set(main_div, [nav, section, form]);
    dom.set(null, main_div);
    for (let msg of messages) {
      messageAdd(msg);
    }
  }

  function loader(show = true) {
    let elem = document.getElementById("loader");
    if (show) {
      elem.classList.remove("hide");
    } else {
      elem.classList.add("hide");
    }
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
    auth: auth,
    loader: loader,

    rooms: rooms,
    messageAdd: messageAdd,
    messageList: messageList,
    showToast: showToast,
    addChat: addChat,
  };
})();

export default ui;
