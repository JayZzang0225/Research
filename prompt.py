import requests
import json
url = "http://localhost:11434/api/generate"
data = {
    "model": "llama3",
    "prompt": """빅데이터(Big Data) 분석 기술이 최근 트렌드에서 어떻게 활용되고 있고, 향후 어떤 인사이트(Insight)를 제공할 것으로 예상하시나요? 한국어로 글자수는 대략 1000자로 답변해주세요.

"""
}

headers = {'Content-Type': 'application/json'}

response = requests.post(url, json=data, headers=headers)

if response.status_code == 200:
    print('Success')

    # 개별 JSON 객체로 분할
    json_objects = response.content.decode().strip().split("\n")

    # 각 JSON 객체를 Python 사전으로 변환
    data = [json.loads(obj) for obj in json_objects]
    res_text = ''
    # 변환된 데이터 출력
    for item in data:
        # print(item)
        res_text += item['response']
        
    print(res_text)

else:
    print("Error:", response.status_code, response.text)


# # Ollama API URL
# API_URL = "http://localhost:11434/api/generate"

# def ollama_prompt(prompt: str, model: str = "llama3"):
#     """
#     Ollama API를 사용하여 프롬프트 실행.

#     Args:
#         prompt (str): 실행할 프롬프트.
#         model (str): 사용할 모델 이름 (기본값: "llama2").

#     Returns:
#         str: 모델의 응답.
#     """
#     headers = {
#         "Content-Type": "application/json",
#     }
#     data = {
#         "model": model,
#         "prompt": prompt,
#     }

#     try:
#         response = requests.post(API_URL, headers=headers, json=data)
#         response.raise_for_status()
#         result = response.json()
#         return result.get("response", "No response from model.")
#     except requests.exceptions.RequestException as e:
#         return f"Error: {e}"

# # 실행 예제
# if __name__ == "__main__":
#     user_prompt = "Explain what RAG is."
#     model_response = ollama_prompt(user_prompt)
#     print("Model Response:")
#     print(model_response)
