import os
from dotenv import load_dotenv

# .env 파일 로드 (선택 사항)
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "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")  # 환경 변수에서 API 키 불러오기
CSV_PATH = os.getenv("CSV_PATH", "D:/research/useopenai/korean_refined_words.csv")  # ✅ 절대경로로 설정
GPT_MODEL = "gpt-4-turbo"  # GPT-4 Turbo 사용
