from flask import Flask, request, jsonify
import os
import openai

# Flaskアプリケーションの初期化
app = Flask(__name__)

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
        return str(e)

# ルートエンドポイントを定義
@app.route("/", methods=["GET"])
def home():
    return "Welcome to Azure OpenAI App!"

# 質問を処理するエンドポイント
@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()  # クライアントからのデータを取得
    prompt = data.get("prompt", "")
    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    result = ask_openai(prompt)
    return jsonify({"response": result})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
