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
    { code: "ta", name: "Tamil" }
  ];

  const handleTranslate = async () => {
    if (!text) return;
    setLoading(true);
    try {
      console.log("Sending request to backend...");
      const response = await axios.post("/translate", {
        text,
        source_lang: sourceLang,
        target_lang: targetLang,
      }, { timeout: 30000 }); // Increase timeout to 30 seconds
      console.log("Response received:", response.data);
      setTranslatedText(response.data.translated_text);
    } catch (error) {
      console.error("Error translating text", error);
      if (error.response) {
        // The request was made and the server responded with a status code
        // that falls out of the range of 2xx
        setTranslatedText(`Error translating text: ${error.response.data.error}`);
      } else if (error.request) {
        // The request was made but no response was received
        setTranslatedText("Error translating text: No response received from server.");
      } else {
        // Something happened in setting up the request that triggered an Error
        setTranslatedText(`Error translating text: ${error.message}`);
      }
    }
    setLoading(false);
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(translatedText);
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 p-4">
      <h1 className="text-4xl font-bold text-blue-600 mb-8">Neural Machine Translation</h1>

      <div className="flex w-full max-w-6xl gap-8">
        {/* Input Box */}
        <div className="flex-1">
          <label className="block text-lg font-semibold mb-2">
            {languages.find((lang) => lang.code === sourceLang)?.name}
          </label>
          <textarea
            className="w-full h-48 p-4 border rounded-lg shadow-sm focus:ring focus:ring-blue-300"
            placeholder="Type text to translate..."
            value={text}
            onChange={(e) => setText(e.target.value)}
          />
        </div>

        {/* Output Box */}
        <div className="flex-1">
          <label className="block text-lg font-semibold mb-2">
            {languages.find((lang) => lang.code === targetLang)?.name}
          </label>
          <div className="w-full h-48 p-4 border rounded-lg shadow-sm bg-gray-50 relative">
            <p className="text-gray-700">
              {loading ? "Translating..." : translatedText || "Translation will appear here..."}
            </p>
            {translatedText && (
              <button
                className="absolute top-2 right-2 text-blue-600 hover:text-blue-800"
                onClick={handleCopy}
              >
                📋 Copy
              </button>
            )}
          </div>
        </div>
      </div>

      {/* Language Selection */}
      <div className="flex gap-8 mt-6">
        <div>
          <label className="block text-sm font-medium mb-1">From</label>
          <select
            className="p-2 border rounded-lg shadow-sm"
            value={sourceLang}
            onChange={(e) => setSourceLang(e.target.value)}
          >
            {languages.map((lang) => (
              <option key={lang.code} value={lang.code}>
                {lang.name}
              </option>
            ))}
          </select>
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">To</label>
          <select
            className="p-2 border rounded-lg shadow-sm"
            value={targetLang}
            onChange={(e) => setTargetLang(e.target.value)}
          >
            {languages.map((lang) => (
              <option key={lang.code} value={lang.code}>
                {lang.name}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Translate Button */}
      <button
        className="mt-6 bg-blue-600 text-white px-6 py-3 rounded-lg shadow-md hover:bg-blue-700 transition duration-200"
        onClick={handleTranslate}
        disabled={loading}
      >
        {loading ? "Translating..." : "Translate"}
      </button>
    </div>
  );
};

export default TranslationApp;