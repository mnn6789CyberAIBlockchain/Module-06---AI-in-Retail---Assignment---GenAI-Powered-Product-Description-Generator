from flask import Flask, render_template, request
import requests

app = Flask(__name__)

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2:1b"


def generate_description(product_name, keywords):
    prompt = f"""
Write a compelling and accurate product description for the following retail product.

Product name: {product_name}
Keywords: {keywords}

Write one short paragraph that naturally incorporates the keywords.
Focus only on the information provided. Do not invent specific features or claims.
Product description:
"""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False
            },
            timeout=60
        )

        response.raise_for_status()
        data = response.json()
        return data.get("response", "").strip()

    except requests.exceptions.RequestException as error:
        return f"Error connecting to the local LLM: {error}"


@app.route("/", methods=["GET", "POST"])
def index():
    description = None

    if request.method == "POST":
        product_name = request.form.get("product_name", "").strip()
        keywords = request.form.get("keywords", "").strip()

        if product_name and keywords:
            description = generate_description(product_name, keywords)
        else:
            description = "Please enter both a product name and keywords."

    return render_template("index.html", description=description)


if __name__ == "__main__":
    app.run(debug=False)
