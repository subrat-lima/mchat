import { setToken, domElem, domText, domSet, showToast } from "./helper.js";

export default class Login {
  constructor() {
    this.uiShow();
  }

  uiShow() {
    let legend = domElem("legend");
    domSet(legend, [domText("login")]);

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

    let submit = domElem("input", { type: "submit", value: "login" });

    let form = domElem("form", {}, { submit: this.apiLogin });
    domSet(form, [legend, fieldset, submit]);
    domSet(null, [form]);
  }

  async apiLogin(e) {
    e.preventDefault();
    let form = e.target;
    let form_data = new FormData();
    form_data.append("username", form.username.value);
    form_data.append("password", form.password.value);

    let response = await fetch("/login", {
      method: "POST",
      body: form_data,
    });
    if (response.status == 200) {
      response = response.json();
      let token = response["access_token"];
      setToken(token);

      showToast("user logged in successfully");
      window.location.replace("/");
    } else {
      response = response.json();
      showToast(response.detail, "error");
    }
  }
}
