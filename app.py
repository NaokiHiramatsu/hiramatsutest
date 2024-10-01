import os
import openai

# 環境変数からAPIキーとエンドポイントを取得
openai.api_key = os.getenv("1d61555403f04a659807a94c197c53fd")
openai.api_base = os.getenv("https://gpt35hiramatsu.openai.azure.com/")

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

if __name__ == "__main__":
    user_input = "What is the capital of Japan?"
    result = ask_openai(user_input)
    print("Azure OpenAIの応答:", result)
