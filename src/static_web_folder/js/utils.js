function changeNavColor(id) {
  document.getElementById(id).style.color = "white";
}

function redirect(path) {
  window.location.replace(path);
}

export default { redirect, changeNavColor };
