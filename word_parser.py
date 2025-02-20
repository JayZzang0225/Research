import pandas as pd
import re
from konlpy.tag import Okt, Komoran

# 1. 형태소 분석기 초기화
okt = Okt()
komoran = Komoran()

# 2. 형태소 분석 및 조사 앞 단어 묶음(청크) 추출 함수
def extract_chunks_with_okt(sentence):
    # 형태소 분석 수행
    tokens = okt.pos(sentence, norm=True, stem=False)
    
    # 조사 앞 단어 묶음을 저장할 리스트
    merged_tokens = []
    temp_chunk = ""  # 조사 앞 단어를 임시 저장할 변수
    
    for i, (word, pos) in enumerate(tokens):
        if pos in ["Noun", "Verb"]:  # 명사 또는 동사라면 뭉텅이(청크)로 묶기
            temp_chunk += word + " "
        elif pos == "Josa":  # 조사가 나오면 앞 단어들과 묶어서 청크로 저장
            if temp_chunk:
                merged_tokens.append((temp_chunk.strip(), "COMPOUND"))  # 청크 저장
                temp_chunk = ""  # 초기화
            merged_tokens.append((word, pos))  # 조사 자체도 추가
        else:
            if temp_chunk:
                merged_tokens.append((temp_chunk.strip(), "COMPOUND"))  # 남은 단어 추가
                temp_chunk = ""  # 초기화
            merged_tokens.append((word, pos))  # 기타 품사는 그대로 추가
    
    if temp_chunk:  # 마지막 남은 단어 추가
        merged_tokens.append((temp_chunk.strip(), "COMPOUND"))

    return merged_tokens

def extract_chunks_with_komoran(sentence):
    # 형태소 분석 수행
    tokens = komoran.pos(sentence)
    
    # 조사 앞 단어 묶음을 저장할 리스트
    merged_tokens = []
    temp_chunk = ""  # 조사 앞 단어를 임시 저장할 변수
    
    for i, (word, pos) in enumerate(tokens):
        # Komoran의 품사 태그는 KoNLPy 태그와 다르므로 적절히 수정 가능
        # 예: NNG (일반명사), VV (동사), JKO (조사) 등
        if pos.startswith("NN") or pos.startswith("VV"):  # 명사 또는 동사라면 뭉텅이(청크)로 묶기
            temp_chunk += word + " "
        elif pos.startswith("J"):  # 조사가 나오면 앞 단어들과 묶어서 청크로 저장
            if temp_chunk:
                merged_tokens.append((temp_chunk.strip(), "COMPOUND"))  # 청크 저장
                temp_chunk = ""  # 초기화
            merged_tokens.append((word, pos))  # 조사 자체도 추가
        else:
            if temp_chunk:
                merged_tokens.append((temp_chunk.strip(), "COMPOUND"))  # 남은 단어 추가
                temp_chunk = ""  # 초기화
            merged_tokens.append((word, pos))  # 기타 품사는 그대로 추가
    
    if temp_chunk:  # 마지막 남은 단어 추가
        merged_tokens.append((temp_chunk.strip(), "COMPOUND"))

    return merged_tokens

# 3. 명사 & 청크 추출 함수 (검색용)
def extract_search_keywords(tokens):
    search_terms = [word for word, pos in tokens if pos in ["Noun", "COMPOUND"]]
    return search_terms


def map_tokens_to_original_sentence(sentence):
    # Komoran으로 형태소 분석
    komoran_tokens = komoran.pos(sentence)
    
    # 매핑 결과를 저장할 리스트
    mapped_tokens = []
    
    # 원문에서 형태소를 찾을 시작 위치
    current_index = 0
    
    # 형태소 분석 결과 순회
    for token, pos in komoran_tokens:
        # 원문에서 token이 나타나는 위치를 current_index부터 찾음
        start_index = sentence.find(token, current_index)
        
        if start_index == -1:
            # 형태소가 원문에 없을 경우 (이상적인 경우엔 발생하지 않음)
            continue
        
        # 끝 위치는 token의 길이만큼 더한 값
        end_index = start_index + len(token)
        
        # 형태소, 품사, 원문 내 시작-끝 위치 저장
        mapped_tokens.append({
            "token": token,
            "pos": pos,
            "start_index": start_index,
            "end_index": end_index
        })
        
        # 다음 형태소를 찾기 위해 current_index를 갱신
        current_index = end_index
    
    return mapped_tokens


# 4. 테스트 문장 리스트
sentences = [
    "오늘은 컴퓨터를 켜서 데이터 분석을 합니다.",
    "파인 다이닝을 예약했어요.",
    "밀 프렙을 준비하는 게 좋겠어.",
    "탬퍼링이 금지되어 있습니다.",
    "소켓에 콘센트를 꽂았는데 버튼이 고장났어요."
]

# # 5. 실행 (태깅 + 조사 앞 단어 묶음 + 검색어 리스트 생성)
# for sentence in sentences:
#     print(f"\n📌 [문장 분석]: {sentence}")
    
#     # Okt 태깅
#     okt_tokens = extract_chunks_with_okt(sentence)
#     okt_search_terms = extract_search_keywords(okt_tokens)
    
#     print("\n🟢 [Okt 태깅 결과]:")
#     for word, pos in okt_tokens:
#         print(f"  - {word}: {pos}")
#     print("\n🔍 [Okt 기반 검색 가능한 키워드]:", okt_search_terms)
    
#     # Komoran 태깅
#     komoran_tokens = extract_chunks_with_komoran(sentence)
#     komoran_search_terms = extract_search_keywords(komoran_tokens)
    
#     print("\n🔵 [Komoran 태깅 결과]:")
#     for word, pos in komoran_tokens:
#         print(f"  - {word}: {pos}")
#     print("\n🔍 [Komoran 기반 검색 가능한 키워드]:", komoran_search_terms)
#     print("=" * 80)

# 5. 실행 (태깅 + 우선순위 검색 로직)
for sentence in sentences:

    # 매핑 결과 실행
    mapped_results = map_tokens_to_original_sentence(sentence)

    # 결과 출력
    for mapped in mapped_results:
        print(f"Token: {mapped['token']}, POS: {mapped['pos']}, Start: {mapped['start_index']}, End: {mapped['end_index']}")


    print(f"\n📌 [문장 분석]: {sentence}")
    
    # Okt 태깅
    okt_tokens = okt.pos(sentence, norm=True, stem=False)
    print("\n🟢 [Okt 태깅 결과]:")
    for word, pos in okt_tokens:
        print(f"  - {word}: {pos}")
    
    # Komoran 태깅
    komoran_tokens = komoran.pos(sentence)
    print("\n🔵 [Komoran 태깅 결과]:")
    for word, pos in komoran_tokens:
        print(f"  - {word}: {pos}")
    
    # 우선순위 검색용 처리
    compounds = []
    nouns = []
    
    # Okt 결과를 순회하며 동사를 찾음
    for okt_word, okt_pos in okt_tokens:
        if okt_pos == "Verb":
            # Komoran 결과에서 대응되는 동사 및 어미 확인
            for kom_word, kom_pos in komoran_tokens:
                if kom_word == okt_word:
                    # 1. 동사가 ETM으로 끝나고 뒤에 명사가 있다면 compound로 저장
                    if kom_pos == "ETM":
                        # ETM으로 끝난다면 다음 Komoran 단어가 명사인지 확인
                        next_index = komoran_tokens.index((kom_word, kom_pos)) + 1
                        if next_index < len(komoran_tokens) and komoran_tokens[next_index][1].startswith("NN"):
                            compounds.append(kom_word + " " + komoran_tokens[next_index][0])
                            break
                    # 2. ETN으로 끝난 경우 명사로 저장
                    elif kom_pos == "ETN":
                        nouns.append(kom_word)
                        break
    
    # 결과 출력
    print("\n🔍 우선순위 검색용 단어:")
    print("  - Compound:", compounds)
    print("  - Nouns:", nouns)
    
    # 검색 시 Compound 우선
    print("\n🔍 검색 로직:")
    if compounds:
        print("Compound 검색 결과:", compounds)
    elif nouns:
        print("Noun 검색 결과:", nouns)
    else:
        print("검색 결과 없음")
    
    print("=" * 80)