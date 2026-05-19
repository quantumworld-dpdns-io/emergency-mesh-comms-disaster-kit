import i18n from "i18next";
import { initReactI18next } from "react-i18next";

i18n.use(initReactI18next).init({
  lng: "en",
  fallbackLng: "en",
  resources: {
    en: { translation: { compose: "Compose", inbox: "Inbox", settings: "Settings" } },
    es: { translation: { compose: "Componer", inbox: "Bandeja", settings: "Ajustes" } },
    "zh-TW": { translation: { compose: "撰寫", inbox: "收件匣", settings: "設定" } }
  }
});

export default i18n;
