# csv_loader.py
# korean_refined_words.csv 파일을 읽어, 외래어(원어) -> 순화어 매핑 딕셔너리를 생성

import csv

def load_refined_words(csv_path):
    foreign_to_native = {}
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            fw = row['외래어'].strip()
            ow = row['원어'].strip()
            rw = row['순화어'].strip()
            
            # [🚨추가] 2글자 이하/1글자 이하인 경우는 스킵
            # (원한다면 3글자 미만도 스킵)
            # 너무 짧은 키가 대부분 문제를 일으킵니다.
            if len(fw) < 2:
                continue
            if len(ow) < 3:
                ow = ""  # skip effectively

            # 나머지는 기존 로직대로
            if fw and rw:
                foreign_to_native[fw] = rw
                foreign_to_native[fw.replace(" ", "")] = rw
            if ow and rw:
                foreign_to_native[ow] = rw
                foreign_to_native[ow.replace(" ", "")] = rw
    
    return foreign_to_native
