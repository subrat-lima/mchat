import { getToken } from "./helper.js";

export default class Contact {
  constructor() {
    console.log("in contact constructor");
    this.uiShow();
  }

  async uiShow() {
    let contacts = await this.apiGetContacts();
    let main = document.querySelector("main");
    let button = document.createElement("button");
    let button_text = document.createTextNode("add contact");
    let ul = document.createElement("ul");
    button.addEventListener("click", this.uiAddContact);

    for (let contact of contacts) {
      let li = document.createElement("li");
      let a = document.createElement("a");
      let text = document.createTextNode(contact["alias"]);
      a.appendChild(text);
      li.appendChild(a);
      ul.appendChild(li);
    }

    button.appendChild(button_text);
    main.innerHTML = "";
    main.appendChild(button);
    main.appendChild(ul);
  }

  uiAddContact() {
    new AddContact();
  }

  async apiGetContacts() {
    let token = getToken();
    let response = await fetch("/contacts/", {
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    });
    if (response.status == 200) {
      let contacts = await response.json();
      return contacts;
    }
  }
}

class AddContact {
  constructor() {
    this.uiShow();
  }

  uiShow() {
    let form = document.createElement("form");
    let legend = document.createElement("legend");
    let legend_text = document.createTextNode("add contact");
    let fieldset = document.createElement("fieldset");
    let username = document.createElement("input");
    let username_label = document.createElement("label");
    let username_text = document.createTextNode("username");
    let alias = document.createElement("input");
    let alias_label = document.createElement("label");
    let alias_text = document.createTextNode("alias");

    let submit = document.createElement("input");
    submit.setAttribute("type", "submit");
    submit.setAttribute("value", "add");

    username.setAttribute("type", "text");
    username.setAttribute("name", "username");
    alias.setAttribute("type", "text");
    alias.setAttribute("name", "alias");

    username_label.appendChild(username_text);
    username_label.appendChild(username);
    alias_label.appendChild(alias_text);
    alias_label.appendChild(alias);
    legend.appendChild(legend_text);
    fieldset.appendChild(username_label);
    fieldset.appendChild(alias_label);

    form.appendChild(legend);
    form.appendChild(fieldset);
    form.appendChild(submit);
    form.addEventListener("submit", this.apiAdd);
    let main = document.querySelector("main");
    main.innerHTML = "";
    main.appendChild(form);
  }

  async apiAdd(e) {
    e.preventDefault();
    let token = getToken();
    let form = e.target;
    let data = {
      username: form.username.value,
      alias: form.alias.value,
    };

    let response = await fetch("/contacts/add", {
      method: "POST",
      body: JSON.stringify(data),
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    });

    if (response.status == 200) {
      window.location.replace("/");
    }
  }
}
