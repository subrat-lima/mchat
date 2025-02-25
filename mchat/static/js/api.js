let api = (function () {
  async function post(url, body, content_type) {
    let attrs = {
      method: "post",
      body: body,
    };
    if (content_type == "json") {
      attrs["body"] = JSON.stringify(body);
      attrs["headers"] = { "Content-Type": "application/json" };
    }
    let response = await fetch(url, attrs).then((resp) => resp.json());

    return response;
  }

  async function register(username, password) {
    let body = {
      username: username,
      password: password,
    };
    return await post("/register", body, "json");
  }

  async function login(username, password) {
    let body = new FormData();
    body.append("username", username);
    body.append("password", password);
    return await post("/login", body);
  }

  return {
    login: login,
    register: register,
  };
})();

export default api;
