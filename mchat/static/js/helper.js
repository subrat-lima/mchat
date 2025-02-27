export function get(key) {
  return localStorage.getItem(`mchat-${key}`);
}

export function set(key, value) {
  localStorage.setItem(`mchat-${key}`, value);
}

export function del(keys = []) {
  for (let key of [...keys]) localStorage.removeItem(`mchat-${key}`);
}

export function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

export function getDisplayDate(utc_date) {
  let date = new Date(utc_date + " UTC");
  let day = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
  let today = new Date();
  today.setHours(0, 0, 0, 0);
  let past_week = new Date();
  past_week.setDate(today.getDate() - 6);
  let display_date = "";
  if (date.getTime() >= today.getTime()) {
    display_date = `${date.getHours()}:${date.getMinutes()}`;
  } else if (date.getTime() >= past_week.getTime()) {
    display_date = `${day[date.getDay()]} ${date.getHours()}:${date.getMinutes()}`;
  } else {
    display_date = date;
  }
  return display_date;
}
