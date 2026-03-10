/* PWA standalone mode support for iOS Safari "Add to Home Screen" */
(function () {
  if (!("standalone" in navigator && navigator.standalone)) return;

  // In standalone mode, <a> links open Safari. Intercept internal links.
  document.addEventListener("click", function (e) {
    var link = e.target.closest("a");
    if (!link) return;
    var href = link.getAttribute("href");
    if (!href || href.startsWith("http") || href.startsWith("mailto:")) return;
    e.preventDefault();
    window.location.href = link.href;
  });
})();
