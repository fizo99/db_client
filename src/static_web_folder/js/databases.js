import util from "./utils.js";

const inputField = () => {
  const form = document.createElement("form");
  form.className = "form-list-element";

  const wrapper = document.createElement("div");
  wrapper.className =
    "mdl-textfield mdl-js-textfield mdl-textfield--floating-label";

  const input = document.createElement("input");
  input.className = "mdl-textfield__input";
  input.type = "text";
  input.id = "newdb";

  const label = document.createElement("label");
  label.className = "mdl-textfield__label";
  label.htmlFor = "newdb";
  label.innerHTML = "New database name";

  wrapper.appendChild(input);
  wrapper.appendChild(label);

  form.appendChild(wrapper);

  const newSaveIcon = saveIcon();
  newSaveIcon.addEventListener("click", async () => {
    if (input.value.includes(".")) {
      alert("Enter database name without extension.");
      return;
    }
    const response = await eel.createDatabase(input.value)();
    alert(response.msg);
    if (response.type == "ok") {
      localStorage.setItem("dbName", input.value + ".db");
      window.location = "./schemas.html";
    }
  });
  form.appendChild(newSaveIcon);

  return form;
};

const checkIcon = () => {
  const icon = document.createElement("i");
  icon.className = "mdl-color-text--green-400 material-icons";
  icon.innerHTML = "done";

  return icon;
};

const saveIcon = () => {
  const icon = document.createElement("i");
  icon.className = "mdl-color-text--blue-400 material-icons";
  icon.innerHTML = "save";

  return icon;
};

const addButton = () => {
  const wrapper = document.createElement("div");
  wrapper.className = "row-right";

  const button = document.createElement("button");
  button.className = "mdl-button mdl-js-button mdl-button--primary";
  button.innerHTML = "Add";

  button.addEventListener("click", () => {
    const newElement = inputField();
    button.parentNode.parentNode.insertBefore(newElement, button.parentNode);
    componentHandler.upgradeDom();
  });

  wrapper.appendChild(button);

  return wrapper;
};

const listItem = (dbName) => {
  const content = document.createElement("div");
  content.className = "mdl-grid demo-content";

  const chart = document.createElement("div");
  chart.className =
    "demo-charts mdl-color--white mdl-shadow--2dp mdl-cell mdl-cell--12-col mdl-grid";
  chart.addEventListener("click", function () {
    localStorage.setItem("dbName", dbName);
    window.location = "./schemas.html";
  });

  const listAction = document.createElement("div");
  listAction.className = "demo-list-action mdl-list";

  const listItem = document.createElement("div");
  listItem.className = "mdl-list__item";

  const listItemContent = document.createElement("span");
  listItemContent.className = "mdl-list__item-primary-content";

  const newTextField = document.createElement("span");
  newTextField.innerHTML = dbName;

  listItemContent.appendChild(newTextField);

  listItem.appendChild(listItemContent);
  listAction.appendChild(listItem);
  chart.appendChild(listAction);
  content.appendChild(chart);

  return content;
};

window.onload = async (e) => {
  await fillList();
  util.changeNavColor("nav_databases");
};

const fillList = async () => {
  const list = document.querySelector("#main");
  const databases = await eel.getDatabases()();

  for (let i = 0; i < databases.length; i++) {
    const newListElement = listItem(databases[i]);
    list.appendChild(newListElement);
  }

  list.appendChild(addButton());
};
