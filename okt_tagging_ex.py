from konlpy.tag import Okt

# 1. 형태소 분석기 초기화
okt = Okt()

# 2. 형태소 태깅 함수
def tag_sentence(sentence):
    # Okt 형태소 분석 결과 (태깅)
    tokens = okt.pos(sentence, norm=True, stem=True)
    return tokens

# 3. 테스트 문장
sentences = [
    "오늘은 컴퓨터를 켜서 데이터 분석을 합니다.",
    "파인 다이닝을 예약했어요.",
    "밀 프렙을 준비하는 게 좋겠어.",
    "탬퍼링이 금지되어 있습니다.",
    "소켓에 콘센트를 꽂았는데 버튼이 고장났어요."
]

# 4. 태깅 실행
for sentence in sentences:
    tagged_tokens = tag_sentence(sentence)
    print(f"[문장]: {sentence}")
    print("[태깅 결과]:")
    for word, tag in tagged_tokens:
        print(f"  {word}: {tag}")
    print("=" * 40)
