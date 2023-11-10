import translations from "./translations.js";

const languageElements = document.querySelectorAll(".current-lang, .lang-dropdown");

languageElements.forEach((element) => {
  element.addEventListener("click", () => {
    const language = element.getAttribute("data-lang");
    setLanguage(language);
    localStorage.setItem("lang", language);
  });
});

document.addEventListener("DOMContentLoaded", () => {
  const language = localStorage.getItem("lang") || "en"; // Default to English if the language is not set
  setLanguage(language);
});

const setLanguage = (language) => {
  const elements = document.querySelectorAll("[data-i18n]");
  elements.forEach((element) => {
    const translationKey = element.getAttribute("data-i18n");
    element.textContent = translations[language][translationKey];
  });

  // Optionally, you can set the direction for right-to-left languages (e.g., Arabic)
  document.dir = language === "ar" ? "rtl" : "ltr";
};
