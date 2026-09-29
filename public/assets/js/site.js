/* Confidence Aviation — progressive enhancements. The site is fully usable without JS:
   the nav is visible, gallery links open the full image, the form falls back to mailto. */
(function () {
  "use strict";
  var doc = document;
  var lang = doc.documentElement.lang === "es" ? "es" : "en";
  var T = {
    en: { close: "Close", prev: "Previous image", next: "Next image", of: "of", dialog: "Image viewer" },
    es: { close: "Cerrar", prev: "Imagen anterior", next: "Imagen siguiente", of: "de", dialog: "Visor de imágenes" }
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

  /* ---- Quote form: validate, then compose an email in the visitor's own mail program ----
     There is no server: nothing is sent or stored by this site. */
  var form = doc.getElementById("contact-form");
  if (form) {
    var F = {
      en: { summary: "Please correct the following:", required: "is required.", email: "Enter a valid email address, for example name@company.com.",
            subject: "Repair quote request", opened: "Your email program should now open with the request. Review it, attach any documents, and send it. If nothing opens, email info@confidenceaviation.com or call 1-305-392-6291.",
            labels: { name: "Name", company: "Company / operator", email: "Email", phone: "Phone", manufacturer: "Manufacturer", model: "Model / description",
                      part: "Part number", serial: "Serial number(s)", qty: "Quantity", aircraft: "Aircraft type / registration", work: "Work requested", aog: "Priority", message: "Reported fault / details" } },
      es: { summary: "Corrija lo siguiente:", required: "es obligatorio.", email: "Ingrese un correo electrónico válido, por ejemplo nombre@empresa.com.",
            subject: "Solicitud de cotización de reparación", opened: "Su programa de correo debería abrirse con la solicitud. Revísela, adjunte los documentos y envíela. Si no se abre, escriba a info@confidenceaviation.com o llame al 1-305-392-6291.",
            labels: { name: "Nombre", company: "Empresa / operador", email: "Correo electrónico", phone: "Teléfono", manufacturer: "Fabricante", model: "Modelo / descripción",
                      part: "Número de parte", serial: "Número(s) de serie", qty: "Cantidad", aircraft: "Tipo de aeronave / matrícula", work: "Trabajo solicitado", aog: "Prioridad", message: "Falla reportada / detalles" } }
    }[lang];
    var summary = form.querySelector(".form-errors");
    var status = form.querySelector(".form-status");
    var labelText = function (el) {
      var l = form.querySelector('label[for="' + el.id + '"]');
      return l ? l.childNodes[0].textContent.trim() : el.name;
    };
    var setError = function (el, msg) {
      var out = doc.getElementById(el.id + "-err");
      if (msg) { el.setAttribute("aria-invalid", "true"); } else { el.removeAttribute("aria-invalid"); }
      if (out) out.textContent = msg || "";
    };
    var check = function (el) {
      var v = el.value.trim();
      if (el.required && !v) return labelText(el) + " " + F.required;
      if (el.type === "email" && v && !el.validity.valid) return F.email;
      return "";
    };
    Array.prototype.forEach.call(form.querySelectorAll("input, textarea"), function (el) {
      el.addEventListener("blur", function () { if (el.getAttribute("aria-invalid")) setError(el, check(el)); });
    });
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var problems = [];
      Array.prototype.forEach.call(form.querySelectorAll("input:not([type=checkbox]), textarea"), function (el) {
        var msg = check(el); setError(el, msg);
        if (msg) problems.push({ el: el, msg: msg });
      });
      summary.textContent = "";
      if (problems.length) {
        var p = doc.createElement("p"); p.textContent = F.summary; summary.appendChild(p);
        var ul = doc.createElement("ul");
        problems.forEach(function (x) {
          var li = doc.createElement("li"), a = doc.createElement("a");
          a.href = "#" + x.el.id; a.textContent = x.msg;
          a.addEventListener("click", function (ev) { ev.preventDefault(); x.el.focus(); });
          li.appendChild(a); ul.appendChild(li);
        });
        summary.appendChild(ul); summary.hidden = false; summary.setAttribute("tabindex", "-1"); summary.focus();
        status.textContent = "";
        return;
      }
      summary.hidden = true;
      var v = function (n) { var el = form.elements[n]; if (!el) return ""; if (el.type === "checkbox") return el.checked ? el.value : ""; return el.value.trim(); };
      var order = ["name", "company", "email", "phone", "manufacturer", "model", "part", "serial", "qty", "aircraft", "work", "aog"];
      var lines = order.filter(function (n) { return v(n); }).map(function (n) { return F.labels[n] + ": " + v(n); });
      var body = lines.join("\n") + "\n\n" + F.labels.message + ":\n" + v("message");
      var subject = F.subject + " – " + [v("manufacturer"), v("part")].filter(Boolean).join(" ") + (v("aog") ? " – AOG" : "");
      window.location.href = "mailto:info@confidenceaviation.com?subject=" + encodeURIComponent(subject) + "&body=" + encodeURIComponent(body);
      status.textContent = F.opened;
    });
  }
})();
