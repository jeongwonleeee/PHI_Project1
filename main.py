from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import random
import pandas as pd  # 엑셀 저장용


# 크롬 드라이버 실행
driver = webdriver.Chrome()

# 엑셀에 저장할 데이터 담을 리스트
data = []

# 1~4페이지 반복
for page in range(1, 5):
    url = f"https://shop.pulmuone.co.kr/shop/goodsList?itemId=5456&page={page}"
    driver.get(url)

    print(f"\n📄 {page}페이지 상품 목록\n")

    time.sleep(random.uniform(1.5, 2.5))

    # 상품 리스트 가져오기
    products = driver.find_elements(By.CLASS_NAME, "item-card")
    print(f"총 {len(products)}개 상품\n")

    # range로 인덱스 순회
    for i in range(len(products)):
        time.sleep(random.uniform(0.5, 1.0))

        product = products[i]

        name_el = product.find_elements(By.CLASS_NAME, "item-name")
        price_el = product.find_elements(By.CLASS_NAME, "item-price")
        discount_el = product.find_elements(By.CLASS_NAME, "item-discount")

        name = name_el[0].text if name_el else "상품명 없음"
        price = price_el[0].text if price_el else "가격 없음"
        discount = discount_el[0].text if discount_el else "0%"


        # NEW/ BEST 태그 추출
        tag_el = product.find_elements(By.CLASS_NAME, "item-label")
        if tag_el:
            tag = tag_el[0].text.strip()
        else:
            tag = "None"


        print(f"[{i + 1}] {name} | 가격: {price} | 할인율: {discount}")



        data.append({
            "페이지": page,
            "상품번호": i + 1,
            "상품명": name,
            "가격": price,
            "할인율": discount,
            "태그": tag
        })


# 드라이버 종료
driver.quit()


# pandas로 엑셀 저장
df = pd.DataFrame(data)
df.to_excel("pulmuone_products_with_tag.xlsx", index=False)




