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

    function updateBallotCount() {
        var form = document.getElementById("vote-form");
        if (!form) return;
        var chip = form.querySelector("[data-sel-count]");
        if (!chip) return;
        var total = form.querySelectorAll(".position-card").length;
        var checked = form.querySelectorAll(".candidate-input:checked").length;
        chip.textContent = checked + " / " + total + " Selected";
    }

    document.addEventListener("change", function (event) {
        var target = event.target;
        if (target && target.classList && target.classList.contains("candidate-input")) {
            updateBallotCount();
        }
    });

    document.addEventListener("htmx:afterswap", updateBallotCount);
    updateBallotCount();
})();