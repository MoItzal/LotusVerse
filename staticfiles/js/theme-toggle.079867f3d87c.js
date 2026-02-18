// =============================
//   THEME TOGGLE JS – FINAL FIX
// =============================
(function () {
    const THEMES = ["calm", "blossom", "neon", "dark", "light"];

    const LABELS = {
        calm: "🌿 Lotus Calm",
        blossom: "🌸 Blossom",
        neon: "✨ Neon",
        dark: "🌑 Dark",
        light: "🌕 Light"
    };

    function clearThemes() {
        THEMES.forEach(t =>
            document.body.classList.remove(`theme-${t}`)
        );
    }

    function applyTheme(theme) {
        document.body.classList.add("theme-transition");

        clearThemes();
        document.body.classList.add(`theme-${theme}`);
        localStorage.setItem("selected-theme", theme);

        const current = document.querySelector(".theme-current");
        if (current) current.textContent = LABELS[theme];

        setTimeout(() => {
            document.body.classList.remove("theme-transition");
        }, 450);
    }

    function init() {
        const selector = document.getElementById("theme-box");
        const current = selector?.querySelector(".theme-current");
        const items = selector?.querySelectorAll(".theme-item");

        if (!selector || !current || !items.length) return;

        /* Abrir / fechar SOMENTE pelo botão */
        current.addEventListener("click", (e) => {
            e.stopPropagation();
            selector.classList.toggle("open");
        });

        /* Aplicar tema */
        items.forEach(item => {
            item.addEventListener("click", (e) => {
                e.stopPropagation();
                applyTheme(item.dataset.theme);
                selector.classList.remove("open");
            });
        });

        /* Fechar ao clicar fora */
        document.addEventListener("click", () => {
            selector.classList.remove("open");
        });

        /* Tema salvo */
        const saved = localStorage.getItem("selected-theme") || "calm";
        applyTheme(saved);
    }

    document.addEventListener("DOMContentLoaded", init);
})();
