let api = (function () {
  async function auth(e) {
    e.preventDefault();
    let form = e.target;
    let url = form.getAttribute("action");
    let attrs = {
      method: "post",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({
        username: form.username.value,
        password: form.password.value,
      }),
    };
    let response = await fetch(url, attrs).then((resp) => resp.json());
    return response;
  }

  return {
    auth: auth,
  };
})();

export default api;
