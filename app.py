import logging
from flask import Flask
import os
import openai

# Flaskアプリケーションの初期化
app = Flask(__name__)

# ログの設定
logging.basicConfig(level=logging.DEBUG)

# 環境変数からAPIキーとエンドポイントを取得
openai.api_key = os.getenv("1d61555403f04a659807a94c197c53fd")
openai.api_base = os.getenv("https://gpt35hiramatsu.openai.azure.com/")

# OpenAIにリクエストを送信する関数
def ask_openai(prompt):
    try:
        response = openai.Completion.create(
            engine="gpt-35-turbo",  # 使用するモデル
            prompt=prompt,
            max_tokens=100
        )
        return response.choices[0].text.strip()
    except Exception as e:
        app.logger.error(f"Error while connecting to OpenAI: {str(e)}")
        return str(e)

# ルートエンドポイントを定義
@app.route("/", methods=["GET"])
def home():
    app.logger.info("Home page accessed")
    return "Welcome to Azure OpenAI App!"

# 質問を処理するエンドポイント
@app.route("/ask", methods=["POST"])
def ask():
    app.logger.info("Ask endpoint accessed")
    data = request.get_json()  # クライアントからのデータを取得
    prompt = data.get("prompt", "")
    if not prompt:
        app.logger.warning("Prompt is missing in the request")
        return jsonify({"error": "Prompt is required"}), 400

    result = ask_openai(prompt)
    return jsonify({"response": result})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
