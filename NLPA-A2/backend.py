from flask import Flask, request, jsonify
from transformers import TFAutoModelForSeq2SeqLM, AutoTokenizer
from flask_cors import CORS
import tensorflow as tf

# Enable mixed precision
# tf.keras.mixed_precision.set_global_policy("mixed_float16")

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests


# Load the pre-trained Google mT5 model
def load_model(source_lang, target_lang):
    if source_lang == "en" and target_lang == "hi":
        model_name = "Helsinki-NLP/opus-mt-en-hi"
    elif source_lang == "hi" and target_lang == "en":
        model_name = "Helsinki-NLP/opus-mt-hi-en"
    else:
        return None, None  # Unsupported language pair

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = TFAutoModelForSeq2SeqLM.from_pretrained(model_name)
    return model, tokenizer


@app.route("/translate", methods=["POST"])
def translate():
    data = request.get_json()
    source_text = data.get("text", "")
    source_lang = data.get("source_lang", "")
    target_lang = data.get("target_lang", "")

    print(f"Received text: {source_text}, Source: {source_lang}, Target: {target_lang}")

    if not source_text:
        return jsonify({"error": "Input text cannot be empty"})

    # Load the model
    model, tokenizer = load_model(source_lang, target_lang)
    if model is None:
        return jsonify({"error": "Unsupported language pair"})

    # Prepare the input
    input_text = f"{source_text}"
    inputs = tokenizer(input_text, return_tensors="tf", padding=True, truncation=True)

    # Generate translation with max_length and max_new_tokens
    outputs = model.generate(
        **inputs, max_new_tokens=50
    )  # Set max_length and max_new_tokens to control the length of the generated text
    print(f"Model Output: {outputs}")  # Check if it's empty
    translated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return jsonify({"translated_text": translated_text})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
