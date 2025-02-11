import pandas as pd
from konlpy.tag import Okt

# 1. CSV 파일 로드
file_path = "korean_refined_words.csv"
df = pd.read_csv(file_path)

# 2. 외래어-순화어 사전 생성
foreign_to_korean = dict(zip(df["외래어"], df["순화어"]))

# 3. 형태소 분석기 초기화
okt = Okt()

# 4. 외래어를 순화어로 변환하는 함수
def replace_foreign_words(sentence, conversion_dict):
    tokens = okt.morphs(sentence, norm=True, stem=False)  # 형태소 분석 (원형 복원 OFF)
    
    converted_tokens = []
    for word in tokens:
        # 사전에 있으면 순화어로 변환, 없으면 그대로 사용
        converted_tokens.append(conversion_dict.get(word, word))

    return "".join([
        " " + word if not word.isalnum() and word != "." else word  # 띄어쓰기 보정
        for word in converted_tokens
    ]).strip()

# 5. 테스트 문장 리스트
sentences = [
    "오늘은 컴퓨터를 켜서 데이터 분석을 합니다.",
    "파인 다이닝을 예약했어요.",
    "밀 프렙을 준비하는 게 좋겠어.",
    "탬퍼링이 금지되어 있습니다.",
    "소켓에 콘센트를 꽂았는데 버튼이 고장났어요."
]

# 6. 변환 실행
for sentence in sentences:
    converted_sentence = replace_foreign_words(sentence, foreign_to_korean)
    print(f"[원문] {sentence}")
    print(f"[변환] {converted_sentence}\n")
