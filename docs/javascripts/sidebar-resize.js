document.addEventListener("DOMContentLoaded", function () {
  var sidebar = document.querySelector(".md-sidebar--primary");
  if (!sidebar || window.innerWidth < 1220) return;

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
  }
});
