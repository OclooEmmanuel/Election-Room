(function () {
    function syncBodyClass(event) {
        var xhr = event.detail.xhr;
        if (!xhr) return;
        var text = xhr.responseText || "";
        var match = text.match(/<body[^>]*\bclass=["']([^"']*)["']/);
        if (match) document.body.className = match[1];
    }

    document.addEventListener("click", function (event) {
        var btn = event.target.closest ? event.target.closest("[data-close-modal]") : null;
        if (!btn) return;
        var overlay = btn.closest(".modal-overlay");
        if (overlay) overlay.style.display = "none";
    });

    document.addEventListener("htmx:afterswap", syncBodyClass);
})();