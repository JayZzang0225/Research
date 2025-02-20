# gpt_refiner.py
import openai
from config import OPENAI_API_KEY

# 구버전이라면 openai.OpenAI(...)를 쓸 수 있으나,
# 최신 openai>=1.0.0 에서는 openai.Client(...) 문법이 필요할 수 있음.
# 여기서는 기존 코드 유지 (구버전 API).
client = openai.OpenAI(api_key=OPENAI_API_KEY)

def refine_sentence_with_gpt(sentence):
    """
    (기존 함수)
    2차 변환 없이 문장을 자연스럽게 다듬어주는 간단한 예시.
    """
    prompt = f"아래 문장을 매끄럽게 다듬어 주세요.\n\n문장: \"{sentence}\""

    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "너는 한국어 문장을 자연스럽게 다듬는 AI야."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=2000,
        temperature=0
    )
    return response.choices[0].message.content.strip()

def replace_foreign_words_via_gpt(sentence, mapping):
    """
    (기존 함수)
    CSV 매핑을 문자열 형태로 GPT에 넘겨, 외래어->순화어 치환을 직접 GPT에 요청하는 예시.
    """
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

def refine_sentence_with_gpt_no_revert(replaced_sentence):
    """
    (신규 함수)
    이미 고유어로 치환된 단어를 절대 다시 외래어로 역치환하지 않도록 지시.
    문장의 조사, 어색한 표현만 교정하고, 의미/뉘앙스는 유지.
    """
    system_content = """
    너는 한국어 텍스트를 전문적으로 교정하고 자연스럽게 다듬는 AI야.
    문장의 외래어를 이미 고유어로 치환한 상태라면,
    그 단어를 다시 외래어로 되돌리지 말아줘.
    문장의 의미나 흐름을 유지하되,
    조사나 어색한 표현만 교정해줘. 원래 문장을 요약하지 말고 전체 문장을 그대로 보여줘
    """

    user_content = f"""
    아래 문장은 1차로 외래어→고유어 치환을 마친 상태입니다.
    이 문장을 자연스럽게 교정하되,
    이미 고유어로 바뀐 단어는 다시 외래어로 바꾸지 말아주세요. 요약하지 말고 전체 문장을 그대로 보여줘.

    문장:
    \"{replaced_sentence}\"
    """

    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content}
        ],
        max_tokens=2000,
        temperature=0
    )
    return response.choices[0].message.content.strip()
