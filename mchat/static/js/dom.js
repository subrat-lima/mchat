let dom = (function () {
  function elem(name, attrs = {}, eventListeners = {}) {
    let elem = document.createElement(name);
    for (let [key, value] of Object.entries(attrs)) {
      if (key == "cls") {
        key = "class";
      }
      elem.setAttribute(key, value);
    }
    for (let [key, value] of Object.entries(eventListeners)) {
      elem.addEventListener(key, value);
    }
    return elem;
  }

  function text(data) {
    return document.createTextNode(data);
  }

  function set(parent = null, children = [], clean = true) {
    if (!parent) {
      parent = document.querySelector("main");
    }
    if (clean) {
      parent.innerHTML = "";
    }
    if (!Array.isArray(children)) {
      children = [children];
    }
    for (let child of children) {
      parent.appendChild(child);
    }
  }

  function link(hash, data, handler) {
    let a = elem("a", { href: hash });
    set(a, text(data));
    set(null, a);
    a.addEventListener("click", handler);
    return a;
  }

  function input(name, type = "text", placeholder = null, add_label = true) {
    if (!placeholder) {
      placeholder = name;
    }
    let e = elem("input", { name: name, type: type, placeholder: placeholder });
    if (add_label) {
      let label = elem("label");
      set(label, [text(name), e]);
      return label;
    } else {
      return e;
    }
  }

  function form(name, inputs, handler) {
    let form = elem("form", {}, { submit: handler });
    let legend = elem("legend");
    let fieldset = elem("fieldset");
    let submit = elem("input", { type: "submit", value: name });
    for (let e of inputs) {
      set(fieldset, [input(e.name, e.type, e.placeholder)], false);
    }

    set(legend, text(name));
    set(form, [legend, fieldset, submit]);
    return form;
  }

  return {
    elem: elem,
    text: text,
    set: set,
    link: link,
    input: input,
    form: form,
  };
})();

export default dom;
