const count = document.getElementById("count");
const events = new EventSource("/countdown");

events.addEventListener("message", (event) => {
  count.textContent = event.data;
});

events.addEventListener("done", (event) => {
  count.textContent = event.data;
  events.close();
});
