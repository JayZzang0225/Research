#CSV를 통해 만든 매핑 딕셔너리를 사용해서, Python 로직(정규표현식, 간단한 split 등)으로 1차 치환하는 기능을 담습니다.

# replace_words.py
# replace_words.py
# CSV 매핑 딕셔너리를 활용해 Python 로직(정규표현식, N-그램 등)으로
# 1차 치환을 수행
# replace_words.py
import re

def strip_punct_particle(token):
    """
    - 문장부호 제거 (.,!?)
    - 조사(을, 를, 은, 는, 이, 가, ...) 제거하여 base / particle 분리
    예: "다이닝을." -> base="다이닝", particle="을", punctuation="."
    """
    # (1) 맨 끝 문장부호 제거
    punctuation_match = re.search(r'[,.!?]+$', token)
    punctuation = punctuation_match.group(0) if punctuation_match else ''
    token_without_punct = token[:-len(punctuation)] if punctuation else token

    # (2) 조사 제거
    # 필요하면 목록 확장
    match = re.match(r'^(.*?)(을|를|은|는|이|가|으로|로|와|과|에도|도)?$', token_without_punct)
    if match:
        base = match.group(1)
        particle = match.group(2) or ''
        return base, particle, punctuation
    else:
        return token, '', ''

def combine_punct_particle(base, particle, punctuation):
    """strip_punct_particle()로 분리한 것을 다시 합쳐주는 함수"""
    return base + particle + punctuation

def replace_foreign_words_n_gram(tokens, mapping):
    """
    N-그램(2단어) 방식으로 토큰을 순회하며
    - 2단어 매핑("파인 다이닝")을 우선 시도
    - 실패하면 1단어 매핑 시도
    """
    result = []
    i = 0
    length = len(tokens)

    while i < length:
        # 첫 번째 토큰 분석
        t1_base, t1_particle, t1_punct = strip_punct_particle(tokens[i])

        if i + 1 < length:
            # 두 번째 토큰이 존재하면 2단어 매핑 확인
            t2_base, t2_particle, t2_punct = strip_punct_particle(tokens[i + 1])

            # "파인" + "다이닝" => "파인 다이닝" / "파인다이닝"
            joined_key = t1_base + " " + t2_base
            joined_key_nospace = t1_base + t2_base

            # 매핑 딕셔너리에 2단어 키가 있는지 확인
            if joined_key in mapping or joined_key_nospace in mapping:
                # 매핑 성공
                val = mapping.get(joined_key) or mapping.get(joined_key_nospace)

                # 조사, 문장부호는 "두 번째 토큰" 기준으로 붙이는 것이 자연스러움
                # "파인 다이닝을" => base="파인 다이닝", particle="을"
                # ex) final_token = "고급 식사" + "을" + t2_punct
                final_token = combine_punct_particle(val, t2_particle, t2_punct)
                
                # 결과에 추가
                result.append(final_token)
                
                i += 2  # 두 개의 토큰을 한 번에 처리
                continue

        # (2) 2단어 매핑 실패 => 1단어 매핑 시도
        # t1_base를 매핑에서 찾기
        t1_base_nospace = t1_base.replace(" ", "")
        if t1_base in mapping or t1_base_nospace in mapping:
            val = mapping.get(t1_base) or mapping.get(t1_base_nospace)
            final_token = combine_punct_particle(val, t1_particle, t1_punct)
            result.append(final_token)
        else:
            # 매핑 실패 => 원본 그대로
            result.append(tokens[i])

        i += 1

    return result

def replace_in_sentence(sentence, mapping):
    """
    최종적으로 문장 -> 토큰 split -> n-gram 치환 -> 다시 합침
    """
    # 유니코드 공백 등 정규화 (필요시)
    # import re
    # sentence = re.sub(r'\s+', ' ', sentence).strip()
    
    tokens = sentence.split()  # 공백 기준 토큰화
    replaced_tokens = replace_foreign_words_n_gram(tokens, mapping)
    return " ".join(replaced_tokens)

