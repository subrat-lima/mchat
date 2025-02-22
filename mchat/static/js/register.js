import { domElem, domText, domSet, showToast } from "./helper.js";

export default class Register {
  constructor() {
    this.uiShow();
  }

  uiShow() {
    let legend = domElem("legend");
    domSet(legend, [domText("register")]);

    let username_label = domElem("label");
    let username = domElem("input", {
      type: "text",
      placeholder: "username",
      name: "username",
    });
    let username_text = domText("username");
    let password_label = domElem("label");
    let password = domElem("input", {
      type: "password",
      placeholder: "password",
      name: "password",
    });
    domSet(username_label, [domText("username"), username]);
    domSet(password_label, [domText("password"), password]);

    let fieldset = domElem("fieldset");
    domSet(fieldset, [username_label, password_label]);

    let submit = domElem("input", { type: "submit", value: "register" });

    let form = domElem("form", {}, { submit: this.apiRegister });
    domSet(form, [legend, fieldset, submit]);
    domSet(null, [form]);
  }

  async apiRegister(e) {
    e.preventDefault();
    let form = e.target;
    let data = {
      username: form.username.value,
      password: form.password.value,
    };

    let response = await fetch("/register", {
      method: "POST",
      body: JSON.stringify(data),
      headers: {
        "Content-Type": "application/json",
      },
    });
    if (response.status == 200) {
      showToast("user registered successfully");
      window.location.replace("/");
    } else {
      response = await response.json();
      showToast(response.detail, "error");
    }
  }
}
