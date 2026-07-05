const themeButton = document.getElementById("theme-toggle");
const themeIcon = document.getElementById("theme-icon");

function applyTheme(theme) {
    document.body.classList.remove("dark", "light");
    document.body.classList.add(theme);
    localStorage.setItem("rulebot-theme", theme);

    if (themeIcon) {
        themeIcon.textContent = theme === "dark" ? "D" : "L";
    }
}

function toggleTheme() {
    const nextTheme = document.body.classList.contains("dark")
        ? "light"
        : "dark";

    applyTheme(nextTheme);
}

applyTheme(localStorage.getItem("rulebot-theme") || "dark");

themeButton.addEventListener("click", toggleTheme);
