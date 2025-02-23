from flask import Flask, request, jsonify
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

app = Flask(__name__)

# Load the pre-trained model (IndicTrans or mT5)
model_name = "ai4bharat/indictrans2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

"""
hf_token = "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"  # Replace with your actual token
tokenizer = AutoTokenizer.from_pretrained(model_name, token=hf_token)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name, token=hf_token)
"""


@app.route("/translate", methods=["POST"])
def translate():
    data = request.get_json()
    source_text = data.get("text", "")
    source_lang = data.get("source_lang", "")
    target_lang = data.get("target_lang", "")

    if not source_text:
        return jsonify({"error": "Input text cannot be empty"})

    # Prepare the input
    input_text = f"<<{source_lang}>> {source_text} <<{target_lang}>>"
    inputs = tokenizer(input_text, return_tensors="pt")

    # Generate translation
    outputs = model.generate(**inputs)
    translated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return jsonify({"translated_text": translated_text})


if __name__ == "__main__":
    app.run(debug=True)
