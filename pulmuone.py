from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import pandas as pd  # 엑셀 저장용

# 크롬 드라이버 실행
driver = webdriver.Chrome()

# 엑셀에 저장할 데이터 담을 리스트
data = []

# 페이지 번호 초기화
page = 1

while True:
    url = f"https://shop.pulmuone.co.kr/shop/goodsList?itemId=5456&page={page}"
    driver.get(url)

    # 동적 슬립
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "item-card"))
    )
    print(f"\n📄 {page}페이지 상품 목록\n")


    # 여러 개의 상품 정보를 한 번에 가져오기
    products = driver.find_elements(By.CLASS_NAME, "item-card")
    if not products:
        break

    print(f"총 {len(products)}개 상품\n")

    # range로 인덱스 순회
    for i in range(len(products)):
        time.sleep(random.uniform(0.5, 1.0))
        product = products[i]

        # 상품 이름, 가격, 할인율
        name_el = product.find_elements(By.CLASS_NAME, "item-name")
        price_el = product.find_elements(By.CLASS_NAME, "item-price")
        discount_el = product.find_elements(By.CLASS_NAME, "item-discount")
        tag_el = product.find_elements(By.CLASS_NAME, "item-label")

        name = name_el[0].text if name_el else "상품명 없음"
        price = price_el[0].text if price_el else "가격 없음"
        discount = discount_el[0].text if discount_el else "0%"
        tag = tag_el[0].text.strip() if tag_el else "None"

        print(f"[{i + 1}] {name} | 가격: {price} | 할인율: {discount}")

        data.append({
            "페이지": page,
            "상품번호": i + 1,
            "상품명": name,
            "가격": price,
            "할인율": discount,
            "태그": tag
        })

    # ✅ 상품 for문이 끝난 후에 페이지 증가
    page += 1

# 드라이버 종료
driver.quit()

# pandas로 엑셀 저장
df = pd.DataFrame(data)
df.to_excel("pulmuone_products_with_tag.xlsx", index=False)