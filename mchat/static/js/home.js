import { getToken, deleteToken, domElem, domText, domSet } from "./helper.js";
import Login from "./login.js";
import Register from "./register.js";

export default class Home {
  constructor(socket = null) {
    this.uiShow();
  }

  uiShow() {
    let p_login = domElem("p");
    let a_login = domElem("a", { href: "/login" }, { click: this.showLogin });
    domSet(a_login, domText("login"));
    domSet(p_login, [a_login, domText(" to start using application")]);

    let p_register = domElem("p");
    let a_register = domElem(
      "a",
      { href: "/register" },
      { click: this.showRegister },
    );
    domSet(a_register, domText("register"));
    domSet(p_register, [a_register, domText(" if you don't have an account")]);

    domSet(null, [p_login, p_register]);
  }

  showLogin(e) {
    e.preventDefault();
    new Login();
  }

  showRegister(e) {
    e.preventDefault();
    new Register();
  }
}
