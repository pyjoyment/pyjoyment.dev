// The page works without JavaScript, as every selection is a page of its own;
// this script swaps <main> instead of loading the page, and draws the links
// between the selected feature and role
document.documentElement.classList.add("js");

const SVG = "http://www.w3.org/2000/svg";
let drawn = new Set();

function center(box, rect, edge) {
  return [rect.left + rect.width / 2 - box.left, rect[edge] - box.top];
}

function curve(svg, key, d) {
  const path = document.createElementNS(SVG, "path");
  path.setAttribute("d", d);
  path.setAttribute("pathLength", "1");
  if (!drawn.has(key)) {
    path.classList.add("draw");
  }
  path.dataset.key = key;
  svg.append(path);
}

function drawLinks() {
  const cloud = document.querySelector(".cloud");
  const svg = cloud?.querySelector(".links");
  if (!svg) {
    return;
  }
  const box = cloud.getBoundingClientRect();
  svg.setAttribute("viewBox", `0 0 ${box.width} ${box.height}`);
  svg.replaceChildren();

  const features = cloud.querySelectorAll(".feature[aria-current]");
  const roles = cloud.querySelectorAll(".role[aria-current]");
  for (const feature of features) {
    const [x1, y1] = center(box, feature.getBoundingClientRect(), "bottom");
    for (const role of roles) {
      const [x2, y2] = center(box, role.getBoundingClientRect(), "top");
      const y = (y1 + y2) / 2;
      curve(
        svg,
        `${feature.dataset.id} ${role.dataset.id}`,
        `M${x1},${y1} C${x1},${y} ${x2},${y} ${x2},${y2}`,
      );
    }
  }

  drawn = new Set([...svg.children].map((path) => path.dataset.key));
}

function select(tab) {
  const tablist = tab.closest("[role=tablist]");
  for (const other of tablist.querySelectorAll("[role=tab]")) {
    const selected = other === tab;
    other.setAttribute("aria-selected", String(selected));
    other.tabIndex = selected ? 0 : -1;
    document.getElementById(other.getAttribute("aria-controls")).hidden =
      !selected;
  }
}

function enhance() {
  for (const code of document.querySelectorAll("main pre code:not(.hljs)")) {
    window.hljs?.highlightElement(code);
  }
  for (const tablist of document.querySelectorAll("[role=tablist]")) {
    select(tablist.querySelector("[aria-selected=true]"));
  }
  drawLinks();
}

async function navigate(url, push, focus) {
  let doc;
  try {
    const res = await fetch(url, { headers: { Accept: "text/html" } });
    if (!res.ok) {
      throw new Error(res.statusText);
    }
    doc = new DOMParser().parseFromString(await res.text(), "text/html");
  } catch {
    window.location.assign(url);
    return;
  }

  const hadExample = document.querySelector(".example");
  document.title = doc.title;
  document
    .querySelector("link[rel=canonical]")
    ?.replaceWith(doc.querySelector("link[rel=canonical]"));
  document.querySelector("main").replaceWith(doc.querySelector("main"));
  if (push) {
    window.history.pushState(null, "", url);
  }
  enhance();

  if (focus) {
    document.querySelector(`[data-id="${focus}"]`)?.focus();
  }
  const example = document.querySelector(".example");
  if (example && !hadExample) {
    example.scrollIntoView({ behavior: "smooth", block: "nearest" });
  }
}

// The code of a file to the clipboard, or selected, for Ctrl-C, where the
// page has no clipboard, as one of HTTP that is not on localhost
async function copy(button) {
  const code = button.closest("figure").querySelector("pre code");
  try {
    await navigator.clipboard.writeText(code.textContent);
  } catch {
    window.getSelection().selectAllChildren(code);
    return;
  }
  button.textContent = "Copied";
  button.classList.add("copied");
  setTimeout(() => {
    button.textContent = "Copy";
    button.classList.remove("copied");
  }, 2000);
}

document.addEventListener("click", (event) => {
  const tab = event.target.closest("[role=tab]");
  if (tab) {
    select(tab);
    return;
  }

  const button = event.target.closest(".copy");
  if (button) {
    copy(button);
    return;
  }

  const link = event.target.closest("a[data-nav]");
  if (
    !link ||
    event.defaultPrevented ||
    event.button !== 0 ||
    event.metaKey ||
    event.ctrlKey ||
    event.shiftKey ||
    event.altKey
  ) {
    return;
  }
  event.preventDefault();
  navigate(link.href, true, link.dataset.id);
});

document.addEventListener("keydown", (event) => {
  const tab = event.target.closest?.("[role=tab]");
  if (!tab || !["ArrowLeft", "ArrowRight"].includes(event.key)) {
    return;
  }
  const tabs = [
    ...tab.closest("[role=tablist]").querySelectorAll("[role=tab]"),
  ];
  const step = event.key === "ArrowRight" ? 1 : -1;
  const next = tabs[(tabs.indexOf(tab) + step + tabs.length) % tabs.length];
  select(next);
  next.focus();
});

window.addEventListener("popstate", () => {
  navigate(window.location.href, false);
});

window.addEventListener("resize", () => {
  drawLinks();
});

document.addEventListener("DOMContentLoaded", enhance);
