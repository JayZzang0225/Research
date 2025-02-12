# OpenAI GPT 모델과 연동하여 문장을 자연스럽게 다듬거나, 직접 치환 요청을 하는 함수를 넣음
# gpt_refiner.py
# OpenAI GPT 모델과 연동하여 문장을 자연스럽게 다듬거나,
# 직접 치환 요청을 하는 함수를 넣은 예시

# OpenAI GPT 모델과 연동하여 문장을 자연스럽게 다듬거나, 직접 치환 요청을 하는 함수를 넣음
import openai
from config import OPENAI_API_KEY  # API 키 가져오기

# OpenAI 클라이언트 객체 생성
client = openai.OpenAI(api_key=OPENAI_API_KEY)

def refine_sentence_with_gpt(sentence):
    prompt = f"아래 문장을 매끄럽게 다듬어 주세요.\n\n문장: \"{sentence}\""

    response = client.chat.completions.create(
        model="gpt-4-turbo",  # 최신 GPT-4 Turbo 사용
        messages=[
            {"role": "system", "content": "너는 한국어 문장을 자연스럽게 다듬는 AI야."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=100,
        temperature=0
    )
    
    return response.choices[0].message.content.strip()

def replace_foreign_words_via_gpt(sentence, mapping):
    # mapping을 문자열로 변환
    mapping_str = "\n".join([f"- {k} -> {v}" for k, v in mapping.items()])
    
    system_prompt = "너는 한국어 텍스트를 전문으로 교정하는 도우미야."
    user_prompt = f"""
    다음은 외래어와 순화어의 대응표야:
    {mapping_str}
    
    위 표를 참고해서 내가 줄 문장에서
    외래어나 원어를 모두 순화어로 바꿔줘.
    문장: "{sentence}"
    """
    
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        max_tokens=100,
        temperature=0
    )
    
    return response.choices[0].message.content.strip()
