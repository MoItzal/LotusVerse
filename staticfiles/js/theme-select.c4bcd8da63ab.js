// ======================================
//       SELECTOR DE TEMA COM LOCALSTORAGE
// ======================================

document.addEventListener("DOMContentLoaded", () => {

    const select = document.getElementById("theme-switcher");
    const themes = ["calm", "blossom", "neon", "dark", "light"];

    if (!select) return;

    // Aplica tema ao body
    function applyTheme(theme) {
        document.body.className = "";
        document.body.classList.add(`theme-${theme}`);
        localStorage.setItem("selected-theme", theme);
    }

    // Troca ao selecionar
    select.addEventListener("change", () => {
        applyTheme(select.value);
    });

    // Carrega o tema salvo
    const saved = localStorage.getItem("selected-theme") || "calm";

    if (themes.includes(saved)) {
        applyTheme(saved);
        select.value = saved;
    }
});
