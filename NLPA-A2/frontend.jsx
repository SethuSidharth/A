import React, { useState } from "react";
import axios from "axios";

const TranslationApp = () => {
  const [text, setText] = useState("");
  const [translatedText, setTranslatedText] = useState("");
  const [sourceLang, setSourceLang] = useState("en");
  const [targetLang, setTargetLang] = useState("hi");
  const [loading, setLoading] = useState(false);

  const languages = [
    { code: "en", name: "English" },
    { code: "hi", name: "Hindi" },
    { code: "ta", name: "Tamil" },
    { code: "te", name: "Telugu" },
    { code: "bn", name: "Bengali" },
    { code: "mr", name: "Marathi" }
  ];

  const handleTranslate = async () => {
    if (!text) return;
    setLoading(true);
    try {
      const response = await axios.post("http://localhost:5000/translate", {
        text,
        source_lang: sourceLang,
        target_lang: targetLang,
      });
      setTranslatedText(response.data.translated_text);
    } catch (error) {
      console.error("Error translating text", error);
    }
    setLoading(false);
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Neural Machine Translation</h1>
      <div className="mb-4">
        <textarea
          className="border p-2 w-full"
          rows="4"
          placeholder="Enter text to translate"
          value={text}
          onChange={(e) => setText(e.target.value)}
        />
      </div>
      <div className="flex space-x-4 mb-4">
        <select className="border p-2" value={sourceLang} onChange={(e) => setSourceLang(e.target.value)}>
          {languages.map((lang) => (
            <option key={lang.code} value={lang.code}>{lang.name}</option>
          ))}
        </select>
        <select className="border p-2" value={targetLang} onChange={(e) => setTargetLang(e.target.value)}>
          {languages.map((lang) => (
            <option key={lang.code} value={lang.code}>{lang.name}</option>
          ))}
        </select>
      </div>
      <button
        className="bg-blue-500 text-white px-4 py-2"
        onClick={handleTranslate}
        disabled={loading}
      >
        {loading ? "Translating..." : "Translate"}
      </button>
      {translatedText && (
        <div className="mt-4 p-2 border">
          <h2 className="text-xl font-bold">Translated Text</h2>
          <p>{translatedText}</p>
        </div>
      )}
    </div>
  );
};

export default TranslationApp;
