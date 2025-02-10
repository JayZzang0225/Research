import torch
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer

# 모델 및 토크나이저 로드
MODEL = "beomi/KoAlpaca-Polyglot-5.8B"

print("🚀 KoAlpaca 모델 로딩 중...")
model = AutoModelForCausalLM.from_pretrained(
    MODEL,
    torch_dtype=torch.float16,  # 빠른 연산을 위해 float16 사용
    low_cpu_mem_usage=True,
).to("cuda")

# 모델 컴파일 (PyTorch 2.0 이상 사용 시)
model = torch.compile(model)

# 토크나이저 로드
tokenizer = AutoTokenizer.from_pretrained(MODEL)

# ✅ `pipeline`을 한 번만 로드 후 계속 사용 (속도 최적화)
pipe = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    device=0,
)

def ask_question(question, context=None, max_new_tokens=1000, temperature=0.7, top_p=0.9):
    """사용자의 질문을 받아 모델이 답변을 생성하는 함수"""
    prompt = f"### 질문: {question}\n\n### 맥락: {context}\n\n### 답변:" if context else f"### 질문: {question}\n\n### 답변:"
    
    response = pipe(
        prompt,
        do_sample=True,
        max_new_tokens=max_new_tokens,
        temperature=temperature,
        top_p=top_p,
        return_full_text=False
    )

    return response[0]["generated_text"]

# ✅ 질문을 여러 개 받을 수 있도록 수정
print("\n💬 KoAlpaca 챗봇 실행 완료! 질문을 입력하세요.")
print("💡 종료하려면 'exit'를 입력하세요.\n")

while True:
    question = input("🙋‍♂️ 질문: ")
    if question.lower() == "exit":
        print("\n👋 챗봇을 종료합니다. 감사합니다!")
        break

    # ✅ `pipeline`을 반복 실행하지 않고 로드된 `pipe` 재사용
    answer = ask_question(question)
    print(f"\n🤖 답변:\n{answer}\n")
