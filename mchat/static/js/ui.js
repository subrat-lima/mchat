import dom from "./dom.js";
import { getDisplayDate } from "./helper.js";

let ui = (function () {
  function home(openLoginHandler, openRegisterHandler) {
    let login = dom.link(
      "#login",
      "login to start using app",
      openLoginHandler,
    );
    let register = dom.link(
      "#register",
      "register if you dont have an account",
      openRegisterHandler,
    );
    dom.set(null, [login, dom.elem("br"), register]);
  }

  function auth(action, submitHandler) {
    let inputs = [{ name: "username" }, { name: "password", type: "password" }];
    let form = dom.form(action, inputs, submitHandler);
    dom.set(null, form);
  }

  function chatList(chats, chatHandler) {
    let section = dom.elem("section");
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
        },
        { click: chatHandler },
      );
      dom.set(article, dom.text(name));
      dom.set(section, article, false);
    }
    dom.set(null, [section]);
    console.log("chatlist ui loaded");
  }

  function messageAdd(msg, current_user) {
    //let { id, sender_id, sender_name, data, type, create_date } = msg;
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

  function messageList(messages, chat, sendMessageHandler, backHandler) {
    let { current_user, receiver_id, type, name } = chat;
    let nav = dom.elem("article");
    let button = dom.elem("span", { cls: "back-btn" }, { click: backHandler });
    let header = dom.elem("strong");
    let section = dom.elem("section", { id: "messages" });
    let form = dom.elem(
      "form",
      { "data-type": type, "data-id": receiver_id },
      { submit: sendMessageHandler },
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

    dom.set(null, [nav, section, form]);
    for (let msg of messages) {
      console.log("msg: ", msg);
      messageAdd(msg, chat.current_user);
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
    auth: auth,
    home: home,
    chatList: chatList,
    messageAdd: messageAdd,
    messageList: messageList,
    loader: loader,
    showToast: showToast,
  };
})();

export default ui;
