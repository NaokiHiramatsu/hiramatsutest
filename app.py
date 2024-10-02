import logging
from flask import Flask, request, jsonify
import os
from openai import AzureOpenAI  # Azure OpenAIクライアントをインポート
import traceback

# Flaskアプリケーションの初期化
app = Flask(__name__)

# ログの設定
logging.basicConfig(level=logging.DEBUG)

# 環境変数からAzure OpenAIの情報を取得
endpoint = os.getenv("ENDPOINT_URL", "https://gpt35hiramatsu.openai.azure.com/")  # デフォルト値を追加
deployment = "text-embedding-ada-002"  # デプロイメント名を直接指定
subscription_key = os.getenv("AZURE_OPENAI_API_KEY")

# Azure OpenAIにリクエストを送信する関数
def ask_openai(prompt):
    try:
        # Azure OpenAIクライアントの初期化
        client = AzureOpenAI(
            azure_endpoint=endpoint,
            api_key=subscription_key,
            api_version="2024-05-01-preview",
        )

        # 埋め込みモデルのリクエスト送信
        response = client.embeddings.create(
            model=deployment,  # 埋め込み用モデルを使用
            input=prompt
        )

        # 埋め込みの結果を返す
        return response['data'][0]['embedding']
    except Exception as e:
        app.logger.error(f"Error while connecting to Azure OpenAI: {str(e)}")
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
    try:
        data = request.get_json()  # クライアントからのデータを取得
    except Exception as e:
        app.logger.error(f"Error processing JSON: {str(e)}")
        return jsonify({"error": "Invalid JSON format"}), 400

    prompt = data.get("prompt", "")
    if not prompt:
        app.logger.warning("Prompt is missing in the request")
        return jsonify({"error": "Prompt is required"}), 400

    result = ask_openai(prompt)
    return jsonify({"response": result})

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))  # Azureでは環境変数からポートを取得
    app.run(host='0.0.0.0', port=port)
