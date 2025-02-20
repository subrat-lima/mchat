import { setToken } from "./helper.js";
import Login from "./login.js";
import Register from "./register.js";

export default class Home {
  constructor() {
    this.addHandlers();
  }

  addHandlers() {
    let login = document.querySelector("#login");
    let register = document.querySelector("#register");
    login.addEventListener("click", this.showLogin);
    register.addEventListener("click", this.showRegister);
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
