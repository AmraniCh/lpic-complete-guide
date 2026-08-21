function initSidebarResize() {
  var sidebar = document.querySelector(".md-sidebar--primary");
  if (!sidebar || window.innerWidth < 1220) return;
  if (sidebar.querySelector(".sidebar-resize-handle")) return;

  var saved = sessionStorage.getItem("sidebar-width");
  if (saved) sidebar.style.width = saved;

  var handle = document.createElement("div");
  handle.className = "sidebar-resize-handle";
  sidebar.appendChild(handle);

  var startX, startW;

  handle.addEventListener("mousedown", function (e) {
    startX = e.clientX;
    startW = sidebar.offsetWidth;
    document.body.style.userSelect = "none";
    document.body.style.cursor = "col-resize";
    document.addEventListener("mousemove", onDrag);
    document.addEventListener("mouseup", onStop);
  });

  function onDrag(e) {
    var w = Math.max(200, Math.min(600, startW + e.clientX - startX));
    sidebar.style.width = w + "px";
  }

  function onStop() {
    document.removeEventListener("mousemove", onDrag);
    document.removeEventListener("mouseup", onStop);
    document.body.style.userSelect = "";
    document.body.style.cursor = "";
    sessionStorage.setItem("sidebar-width", sidebar.style.width);
  }
}

document.addEventListener("DOMContentLoaded", initSidebarResize);
document.addEventListener("DOMContentSwitch", initSidebarResize);

var observer = new MutationObserver(function () {
  var sidebar = document.querySelector(".md-sidebar--primary");
  if (sidebar && !sidebar.querySelector(".sidebar-resize-handle")) {
    initSidebarResize();
  }
});
observer.observe(document.body, { childList: true, subtree: true });
