document.addEventListener("DOMContentLoaded", function () {
    const textarea = document.querySelector("#texto");
    const counter = document.querySelector("#word-count");

    console.log("Textarea:", textarea);
    console.log("Counter:", counter);

    if (!textarea || !counter) {
        console.error("Elementos não encontrados");
        return;
    }

    function countWords(text) {
        return text.trim() === ""
            ? 0
            : text.trim().split(/\s+/).length;
    }

    function updateCounter() {
        counter.textContent = countWords(textarea.value);
    }

    textarea.addEventListener("input", updateCounter);

    // Atualiza ao carregar
    updateCounter();
});
