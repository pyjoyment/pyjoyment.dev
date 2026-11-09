// ws: of http: and wss: of https:
const url = new URL("/echo", window.location.href);
url.protocol = url.protocol.replace("http", "ws");
const ws = new WebSocket(url);
const input = document.getElementById("message");
const log = document.getElementById("log");

ws.addEventListener("message", (event) => {
  const item = document.createElement("li");
  item.textContent = event.data;
  log.append(item);
});

input.addEventListener("keydown", (event) => {
  if (event.key === "Enter" && input.value) {
    ws.send(input.value);
    input.value = "";
  }
});
