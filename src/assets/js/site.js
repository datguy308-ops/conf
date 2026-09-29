/* Confidence Aviation — progressive enhancements. The site is fully usable without JS:
   the nav is visible, gallery links open the full image, the form falls back to mailto. */
(function () {
  "use strict";
  var doc = document;
  var lang = doc.documentElement.lang === "es" ? "es" : "en";
  var T = {
    en: { close: "Close", prev: "Previous image", next: "Next image", of: "of", dialog: "Image viewer",
          sent: "Your email app should now open with this message. If it does not, email info@confidenceaviation.com.",
          missing: "Please fill in the required fields." },
    es: { close: "Cerrar", prev: "Imagen anterior", next: "Imagen siguiente", of: "de", dialog: "Visor de imágenes",
          sent: "Su aplicación de correo debería abrirse con este mensaje. Si no se abre, escriba a info@confidenceaviation.com.",
          missing: "Complete los campos obligatorios." }
  }[lang];

  /* ---- Mobile navigation ---- */
  var toggle = doc.querySelector(".nav-toggle");
  var nav = doc.getElementById("site-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = toggle.getAttribute("aria-expanded") === "true";
      toggle.setAttribute("aria-expanded", String(!open));
      nav.classList.toggle("is-open", !open);
    });
    doc.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && toggle.getAttribute("aria-expanded") === "true") {
        toggle.setAttribute("aria-expanded", "false");
        nav.classList.remove("is-open");
        toggle.focus();
      }
    });
  }

  /* ---- Lightbox (native <dialog>) ---- */
  var groups = {};
  Array.prototype.forEach.call(doc.querySelectorAll("a[data-lightbox]"), function (a) {
    var g = a.getAttribute("data-lightbox") || "default";
    (groups[g] = groups[g] || []).push(a);
  });
  if (Object.keys(groups).length && typeof HTMLDialogElement === "function") {
    var dlg = doc.createElement("dialog");
    dlg.className = "lightbox";
    dlg.setAttribute("aria-label", T.dialog);
    dlg.innerHTML =
      '<div class="lightbox__inner">' +
        '<div class="lightbox__bar"><span class="lightbox__count" aria-live="polite"></span>' +
        '<button type="button" class="lightbox__close">' + T.close + ' <span aria-hidden="true">&times;</span></button></div>' +
        '<div class="lightbox__stage">' +
          '<button type="button" class="lightbox__prev" aria-label="' + T.prev + '"><span aria-hidden="true">&#8592;</span></button>' +
          '<img alt="">' +
          '<button type="button" class="lightbox__next" aria-label="' + T.next + '"><span aria-hidden="true">&#8594;</span></button>' +
        '</div>' +
        '<p class="lightbox__caption"></p>' +
      '</div>';
    doc.body.appendChild(dlg);
    var img = dlg.querySelector("img");
    var cap = dlg.querySelector(".lightbox__caption");
    var count = dlg.querySelector(".lightbox__count");
    var prev = dlg.querySelector(".lightbox__prev");
    var next = dlg.querySelector(".lightbox__next");
    var list = [], idx = 0, opener = null;

    var show = function (i) {
      idx = (i + list.length) % list.length;
      var a = list[idx];
      var thumb = a.querySelector("img");
      img.src = a.getAttribute("href");
      img.alt = thumb ? thumb.alt : "";
      cap.textContent = a.getAttribute("data-caption") || "";
      count.textContent = list.length > 1 ? (idx + 1) + " " + T.of + " " + list.length : "";
      prev.hidden = next.hidden = list.length < 2;
    };
    Object.keys(groups).forEach(function (g) {
      groups[g].forEach(function (a, i) {
        a.addEventListener("click", function (e) {
          if (e.ctrlKey || e.metaKey || e.shiftKey || e.button !== 0) return;
          e.preventDefault();
          opener = a; list = groups[g]; show(i);
          dlg.showModal();
          dlg.querySelector(".lightbox__close").focus();
        });
      });
    });
    prev.addEventListener("click", function () { show(idx - 1); });
    next.addEventListener("click", function () { show(idx + 1); });
    dlg.querySelector(".lightbox__close").addEventListener("click", function () { dlg.close(); });
    dlg.addEventListener("click", function (e) { if (e.target === dlg || e.target.classList.contains("lightbox__stage")) dlg.close(); });
    dlg.addEventListener("keydown", function (e) {
      if (e.key === "ArrowLeft") { e.preventDefault(); show(idx - 1); }
      else if (e.key === "ArrowRight") { e.preventDefault(); show(idx + 1); }
    });
    dlg.addEventListener("close", function () { img.removeAttribute("src"); if (opener) opener.focus(); });
  }

  /* ---- Contact form: compose an email in the visitor's mail app ---- */
  var form = doc.getElementById("contact-form");
  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var status = form.querySelector(".form-status");
      if (!form.checkValidity()) { status.textContent = T.missing; form.reportValidity(); return; }
      var v = function (n) { return (form.elements[n] && form.elements[n].value || "").trim(); };
      var body = [v("message"), "", "--", v("name"), v("company"), v("phone"), v("email")]
        .filter(function (x, i) { return i < 3 || x; }).join("\n");
      window.location.href = "mailto:info@confidenceaviation.com?subject=" +
        encodeURIComponent(v("subject")) + "&body=" + encodeURIComponent(body);
      status.textContent = T.sent;
    });
  }
})();
