# 전체 흐름을 제어하는 진입점(Entry Point) 스크립트
# CSV 로딩 → 2) 문장 입력(또는 파일에서 가져오기) → 3) Python 기반 치환 → 4) GPT 기반 다듬기 → 5) 결과 출력/저장 등의 순서로 실행
# main.py
# main.py
# 전체 흐름을 제어하는 진입점(Entry Point) 스크립트
# CSV 로딩 → 문장 입력 → Python 기반 치환(1차) → GPT 기반 다듬기(2차) → 결과 출력
# main.py
from config import OPENAI_API_KEY, CSV_PATH
import openai

from csv_loader import load_refined_words
# replace_in_sentence 함수가 구현된 replace_words.py (또는 replace_words_n_gram.py) 임포트
from replace_words import replace_in_sentence
from gpt_refiner import refine_sentence_with_gpt

def main():
    # 1) OpenAI API 설정
    openai.api_key = OPENAI_API_KEY
    
    # 2) CSV 로딩 -> 매핑 딕셔너리 생성
    foreign_to_native = load_refined_words(CSV_PATH)
    
    # 3) 여러 개의 예시 문장
    input_sentences = [
        "오늘은 컴퓨터를 켜서 데이터 분석을 합니다.",
        "파인 다이닝을 예약했어요.",
        "밀 프렙을 준비하는 게 좋겠어.",
        "탬퍼링이 금지되어 있습니다.",
        "소켓에 콘센트를 꽂았는데 버튼이 고장났어요."
    ]
    
    # 4) 각 문장에 대해 치환 + GPT로 다듬기
    for idx, original_sentence in enumerate(input_sentences, start=1):
        # (A) 1차 치환
        replaced_sentence = replace_in_sentence(original_sentence, foreign_to_native)
        # (B) GPT로 문장 다듬기 (최종 결과)
        refined_sentence = refine_sentence_with_gpt(replaced_sentence)
        
        # 5) 결과 출력 (원본문장, 1차 치환, 최종 결과)
        print(f"\n[문장 {idx}] 원본 문장: {original_sentence}")
        print(f"1차 치환: {replaced_sentence}")
        print(f"최종 결과: {refined_sentence}")

if __name__ == "__main__":
    main()
