/* ===============================
   PETALS.JS – CINEMATIC FIX
   =============================== */

(() => {
  const PETAL_CONFIG = {
    calm: "/static/img/petals/calm",
    blossom: "/static/img/petals/blossom",
    neon: "/static/img/petals/neon",
    dark: "/static/img/petals/dark",
    light: "/static/img/petals/light",
  };

  const MAX_PETALS = 28;      // mais pétalas
  const VARIANTS = 24;
  const INTERVAL = 900;      // fluxo constante

  const container = document.getElementById("petals-container");
  if (!container) return;

  function getTheme() {
    return (
      Object.keys(PETAL_CONFIG).find(t =>
        document.body.classList.contains(`theme-${t}`)
      ) || "calm"
    );
  }

  function rand(min, max) {
    return Math.random() * (max - min) + min;
  }

  function createPetal() {
    if (container.children.length >= MAX_PETALS) return;

    const petal = document.createElement("img");
    const theme = getTheme();
    const index = Math.floor(Math.random() * VARIANTS) + 1;

    petal.src = `${PETAL_CONFIG[theme]}/petal_${index}.svg`;
    petal.className = "petal";

    /* 🔑 espalhamento REAL (fora da área central também) */
    petal.style.left = `${rand(-10, 110)}vw`;

    petal.style.animationDuration = `${rand(20, 34)}s`;

    container.appendChild(petal);

    petal.addEventListener("animationend", () => {
      petal.remove();
    });
  }

  setInterval(createPetal, INTERVAL);
})();
