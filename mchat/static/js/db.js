let db = (function () {
  let request = indexedDB.open("mchat", 1);
  let db;

  request.onupgradeneeded = function () {
    let db = request.result;
    let users = db.createObjectStore("users", { keyPath: "id" });
    let usernameIndex = users.createIndex("by_username", "username", {
      unique: true,
    });
    let syncs = db.createObjectStore("syncs", { keyPath: "id" });
    let lastUpdateIndex = syncs.createIndex("by_lastupdate", "last_update");
  };

  request.onsuccess = function () {
    db = request.result;
  };

  function addUsers(users) {
    let tx = db.transaction(["users", "syncs"], "readwrite");
    let user_store = tx.objectStore("users");
    let syncs_store = tx.objectStore("syncs");
    for (let user of [...users]) {
      user_store.put({ id: user.id, username: user.username });
    }
    syncs_store.put({ id: "contacts", last_update: new Date() - 0 });
    tx.oncomplete = function () {
      console.log(`added users to db`);
    };
  }

  function getUsers() {
    let tx = db.transaction("users", "readwrite");
    let users = tx.objectStore("users");
    let index = users.index("id");
    let request = index.openCursor();
    request.cursor = function () {
      let cursor = request.result;
      if (cursor) {
        report(cursor.value.id, cursor.value.username);
        cursor.continue();
      } else {
        report(null);
      }
    };
  }

  return { db: db, addUsers: addUsers, getUsers: getUsers };
})();

export default db;
