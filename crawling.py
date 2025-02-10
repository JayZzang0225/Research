from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import os

# Chrome 웹드라이버 설정
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # 창 없이 실행
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

CHROMEDRIVER_PATH = "C:/Users/Eunsil/Documents/Research/chromedriver-win64/chromedriver.exe"
service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=options)

print("✅ ChromeDriver가 정상적으로 실행되었습니다!")

# URL 설정
base_url = "https://www.korean.go.kr/front/imprv/refineList.do?mn_id=158&pageIndex={}"

# 기존 CSV 파일이 있는 경우 불러오기 (이어서 크롤링 가능)
csv_filename = "korean_refined_words_selenium.csv"
if os.path.exists(csv_filename):
    df_existing = pd.read_csv(csv_filename, encoding="utf-8-sig")
    existing_pages = df_existing["번호"].astype(str).tolist()  # 기존에 수집한 번호 리스트
    print(f"📂 기존 데이터 {len(df_existing)}개 로드됨. 이어서 크롤링 시작!")
else:
    df_existing = pd.DataFrame(columns=["번호", "외래어", "원어", "순화어"])
    existing_pages = []
    print("🆕 새 데이터 수집 시작!")

# 데이터 저장 리스트
data = []

# 페이지 설정 (기존 데이터가 있다면  시작)
start_page = 201  # 원하는 시작 페이지
end_page = 1821    # 원하는 종료 페이지

# 여러 페이지 크롤링
for page in range(start_page, end_page + 1):  
    url = base_url.format(page)
    driver.get(url)

    # 데이터가 로딩될 때까지 대기
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table[data-brl-use='TH'] tbody tr"))
        )
        time.sleep(2)  # 추가 대기 시간 (데이터가 안정적으로 로딩되도록)
    except:
        print(f"⚠️ 페이지 {page}: 테이블이 로딩되지 않음. 건너뜁니다.")
        continue  # 다음 페이지로 이동

    # 테이블 행 찾기
    rows = driver.find_elements(By.CSS_SELECTOR, "table[data-brl-use='TH'] tbody tr")
    page_data = []  # 현재 페이지의 데이터 저장

    for row in rows:
        cols = row.find_elements(By.TAG_NAME, "td")
        if len(cols) >= 4:
            번호 = cols[0].text.strip()
            외래어 = cols[1].text.strip()
            원어 = cols[2].text.strip()
            순화어 = cols[3].text.strip()

            # 기존 데이터에 없는 경우에만 추가
            if 번호 not in existing_pages:
                page_data.append([번호, 외래어, 원어, 순화어])
            else:
                print(f"🔄 페이지 {page}: 중복 데이터 {번호} 건너뜀.")

    if page_data:
        data.extend(page_data)  # 전체 데이터 리스트에 추가
        print(f"✅ 페이지 {page}/{end_page} 완료! {len(page_data)}개 추가됨.")
    else:
        print(f"⚠️ 페이지 {page}: 새로운 데이터 없음.")

# 드라이버 종료
driver.quit()

# 새 데이터가 있을 경우, 기존 데이터와 합치기
if data:
    df_new = pd.DataFrame(data, columns=["번호", "외래어", "원어", "순화어"])
    df_final = pd.concat([df_existing, df_new], ignore_index=True)
    df_final.to_csv(csv_filename, index=False, encoding="utf-8-sig")
    print(f"🚀 크롤링 완료! 총 {len(df_new)}개 추가됨. 최종 데이터 {len(df_final)}개 저장됨.")
else:
    print("📌 새로운 데이터가 없어서 파일을 업데이트하지 않았습니다.")
