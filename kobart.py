from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

# KoBART 모델 로드 (ignore_mismatched_sizes=True 설정 추가)
model_name = "gogamza/kobart-base-v2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name, ignore_mismatched_sizes=True)

# GPU 자동 감지
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

# 입력 문장
text = "AI에 대해 설명해 주세요."
inputs = tokenizer(text, return_tensors="pt", padding="longest", truncation=True, max_length=128).to(device)

# token_type_ids 제거 (BART 모델에서는 필요 없음)
inputs.pop("token_type_ids", None)

# 문장 생성
outputs = model.generate(
    **inputs,
    max_length=128,
    num_beams=5,
    early_stopping=True,
    do_sample=True,
    top_k=50,
    top_p=0.95,
    no_repeat_ngram_size=2,
    repetition_penalty=1.2,
    bos_token_id=tokenizer.bos_token_id,
    eos_token_id=tokenizer.eos_token_id
)

# 결과 디코딩
decoded_text = tokenizer.decode(outputs[0], skip_special_tokens=True, clean_up_tokenization_spaces=True)
print(f"KoBART Output: {decoded_text}")
