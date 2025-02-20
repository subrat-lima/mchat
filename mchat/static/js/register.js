export default class Register {
  constructor() {
    this.uiShow();
  }

  uiShow() {
    let form = document.createElement("form");
    form.classList.add("container");
    let legend = document.createElement("legend");
    let legend_text = document.createTextNode("register");
    let username_label = document.createElement("label");
    let username_text = document.createTextNode("username");
    let username = document.createElement("input");
    username.setAttribute("type", "text");
    username.setAttribute("placeholder", "username");
    username.setAttribute("name", "username");
    let password_label = document.createElement("password");
    let password_text = document.createTextNode("password");
    let password = document.createElement("input");
    password.setAttribute("type", "password");
    password.setAttribute("placeholder", "password");
    password.setAttribute("name", "password");
    let submit = document.createElement("input");
    submit.setAttribute("type", "submit");
    submit.setAttribute("value", "register");
    username_label.appendChild(username_text);
    username_label.appendChild(username);
    password_label.appendChild(password_text);
    password_label.appendChild(password);
    let fieldset = document.createElement("fieldset");

    legend.appendChild(legend_text);
    fieldset.appendChild(username_label);
    fieldset.appendChild(password_label);
    form.appendChild(legend);
    form.appendChild(fieldset);
    form.appendChild(submit);
    form.addEventListener("submit", this.apiRegister);
    let main = document.querySelector("main");
    main.innerHTML = "";
    main.appendChild(form);
  }

  async apiRegister(e) {
    e.preventDefault();
    let form = e.target;
    let form_data = new FormData();
    form_data.append("username", form.username.value);
    form_data.append("password", form.password.value);
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
      window.location.replace("/");
    }
  }
}
