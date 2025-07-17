# Pulmuone Scraper & DB Inserter
이 프로젝트는 Python Selenium을 이용해서
**풀무원 쇼핑몰의 상품 데이터를 자동으로 수집** 하고,
그 결과를 **엑셀 파일로 저장한 뒤, MariaDB에 삽입하는 작업** 입니다.

-----

**엑셀 파일만을 원하면 main.py만 실행합니다.**

**데이터베이스까지 확인하고 싶다면 1. main.py 2. insert_pulmuone_data.py 순서대로 실행해주셔야 하고
2번 실행 전 dBeaver에서 테이블을 먼저 생성해야합니다.**

# 사용 기술
- 개발 언어
    - Python
- 주요 라이브러리
    - Selenium (웹페이지 자동화)
    - pandas (데이터 분석)
    - openpyxl (엑셀 저장)
    - pymysql (DB 연결)
    - matplotlib (그래프)
- 개발 환경 
    - Pycharm
    - DBeaver
- 활용 드라이버
  - chromeDriver

# 사용 방법
Pulmuone Scraper를 사용하기 위한 방법과 을 나열합니다.

사용 방법은 IDE(Pycharm, DBeaver), MariaDB를 통한 방법과 CMD에서 실행하는 2가지 방법이 있습니다.

## 사전 설치 항목 
1. Python 설치
   - Link: [https://www.python.org/downloads/](https://www.python.org/downloads/)

2. ChromeDriver 설치
   - Link: [ https://sites.google.com/chromium.org/driver/](https://sites.google.com/chromium.org/driver/)

3. Pycharm 설치(Option)
   - Link: [pycharm](https://www.jetbrains.com/pycharm/download/?section=windows)
  
4. MariaDB 설치
   - Link: [mariaDB](https://mariadb.org/download/?t=mariadb&p=mariadb&r=11.8.2&os=windows&cpu=x86_64&pkg=msi&mirror=blendbyte)
   - root 비밀번호 설정
   - 포트 번호
   - 서비스 등록

## 실행 방법

### Pycharm에서 실행하기
1. Git pull
```bash
git clone https://github.com/jeongwonleeee/PHI_Project1.git
```

2. Pycharm 실행
- git repository 내 main.py 파일 붙여넣기
- 실행

### CMD 창에서 실행하기
1. main.py
    1-1. Git pull
    ```bash
    git clone https://github.com/jeongwonleeee/PHI_Project1.git
    ```
    1-3. selenium 설치 (Option)
    ```bash
    pip install selenium
    ```
    1-4. pandas 설치 (Option)
    ```bash
    pip install pandas
    ```
    1-5 openpyxl 설치 (Option)
    ```bash
    pip install openpyxl
    ```
    1-6. Python 파일 실행
    ```bash
    cd PHI_Project1
    python3 main.py
    ```

2. insert_pulmuone_data.py

    2-1 DBeaver 설치 (Option)
    - Link:[DBeaver](https://dbeaver.io/download/)
    - New Database Connection
    - MariaDB 선택
    - 정보 입력
  
    2-2 엑셀 파일 준비
    - 파일명: `pulmuone_products_with_tag.xlsx`
    - 위치:`C:/Users/pa/PyCharmMiscProject/` 또는 코드에서 지정한 경로에 위치
  
    2-3 Python 파일 실행
    ```bash
    cd PHI_Project1
    python3 insert_pulmuone_data.py
    ```
3. tag.py
   - matplotlib 라이브러리 설치 (pycharm or cmd)
      ```bash
    pip install matplotlib
    ```

# 주요 코드 설명

## 크롬 웹드라이버 실행
driver = webdriver.Chrome()
웹페이지를 자동으로 조작하기 위해 크롬 창을 띄웁니다.

### 1~4페이지 반복
```python
for page in range(1,5)
url = f"https://shop.pulmuone.co.kr/shop/goodsList?itemId=5456&page={page}"
    driver.get(url)
 ```


```python
print(f"\n📄 {page}페이지 상품 목록\n)
time.sleep(random.uniform(1.5, 2.5))
```

uniform을 사용하여 1.5 이상 2.5 이하 범위의 실수를 직접 지정해서 리턴합니다.

random.random() 함수보다 훨씬 간단하고 직관적입니다.


### 여러 개의 상품 정보를 한 번에 가져오기
```python
    products = driver.find_elements(By.CLASS_NAME, "item-card")
    print(f"총 {len(products)}개 상품\n")
```

크롤링할 요소를 찾기 위해 HTML 구조 속 클래스명이나 태그명이 필요합니다.

item-card는 찾고자 하는 요소의 클래스 이름입니다.

### range로 인덱스 순회
 ```python
    for i in range(len(products)):
        time.sleep(random.uniform(0.5, 1.0))

        product = products[i]

        name_el = product.find_elements(By.CLASS_NAME, "item-name")
        price_el = product.find_elements(By.CLASS_NAME, "item-price")
        discount_el = product.find_elements(By.CLASS_NAME, "item-discount")
```
클래스가 있으면, 리스트로 리턴됩니다.

클래스가 없으면, [] (빈 리스트)로 리턴되어 에러 안 나고 계속 실행됩니다.

```python
        name = name_el[0].text if name_el else "상품명 없음"
        price = price_el[0].text if price_el else "가격 없음"
        discount = discount_el[0].text if discount_el else "0%"
```
name_el이 비어 있지 않으면 [0].text로 값 꺼내기

비어있으면, "상품명 없음" 이라는 기본값 사용합니다

모든 상품에 모든 정보가 무조건 있다고 가정할 시, 크롤링 중간에 멈추는 오류가 발생합니다.

오류 방지를 위해 find-elements() + 조건문 if-else로 크롤링 해줘야 합니다.

### 상품 이미지 옆 NEW/ BEST 태그 추출
```python
        tag_el = product.find_elements(By.CLASS_NAME, "item-label")
        if tag_el:
            tag = tag_el[0].text.strip()
        else:
            tag = "None"


        print(f"[{i + 1}] {name} | 가격: {price} | 할인율: {discount}")
```

if 태그 있으면 추출하고,
else: 태그가 없다면, "None"으로 처리됩니다.

```python
data.append({
            "페이지": page,
            "상품번호": i + 1,
            "상품명": name,
            "가격": price,
            "할인율": discount,
            "태그": tag
        })
```
크롤링한 정보를 한 줄의 딕셔너리로 만들고, 데이터 리스트에 하나씩 추가합니다.

### 드라이버 종료
```python
driver.quit()
```

### pandas로 엑셀 저장
```python
df = pd.DataFrame(data)
df.to_excel("pulmuone_products_with_tag.xlsx", index=False)
```

### 엑셀 파일 불러오기
```python
import pandas as pd
import pymysql
df = pd.read_excel("pulmuone_products_with_tag.xlsx")
```
### DB 연결
```python
conn = pymysql.connect(
    host='localhost',
    user='your_db_user',
    password='your_db_password',
    db='your_db_name',
    charset='utf8mb4',
    autocommit=True
)
cursor = conn.cursor()
```
실제 사용할 때는 user, password, db를 본인의 정보로 바꿔야 합니다.

# 데이터 삽입 반복
```python
for i, row in df.iterrows():
    sql = """
    INSERT INTO `pulmuone-products` (name, price, discount_rate, tag)
    VALUES (%s, %s, %s, %s)
    """
    cursor.execute(sql, (
        row['상품명'],
        int(str(row['가격']).replace(',', '')),
        str(row['할인율']),
        str(row['태그'])
    ))
```
가격은 엑셀에 쉼표(,)가 포함되어 있을 수 있으므로 str(row['가격']).replace(',', '')를 사용해

쉼표를 제거한 후 int()로 정수형으로 변환합니다.

### DB 연결 종료
```python
cursor.close()
conn.close()
print("✅ 데이터 삽입 완료!")
```

# `BEST 상품`과 `일반 상품`의 평균 할인율을 비교 결과
### 라이브러리
```python
import pandas as pd
import matplotlib.pyplot as plt #그래프를 그리기 위한 라이브러리
import matplotlib.font_manager as fm #한글 폰트 깨짐 방지를 위한 설정용
import platform
```
### 엑셀 파일 불러오기
```python
df = pd.read_excel("pulmuone_products_with_tag.xlsx")
```
### 할인율을 숫자로 바꾸기
```python
df['할인율(숫자)'] = df['할인율'].str.replace('%', '').astype(int)
```
### Best 상품과 일반 상품 나누기
```python
best_avg = df[df['태그'] == 'BEST']['할인율(숫자)'].mean()
non_best_avg = df[df['태그'] != 'BEST']['할인율(숫자)'].mean()
labels = ['BEST 상품', '일반 상품']
discounts = [best_avg, non_best_avg]
```
### 그래프 그리기
```python
plt.figure(figsize=(8, 6))
bars = plt.bar(labels, discounts, color=['skyblue', 'lightgray'])

for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, height + 0.5, f'{height:.1f}%', ha='center', fontsize=12)

plt.title('BEST 상품 vs 일반 상품 평균 할인율 비교', fontsize=15)
plt.ylabel('평균 할인율 (%)', fontsize=12)
plt.ylim(0, max(discounts) + 5)
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.tight_layout()
```

### 그래프 저장하기 (Option)
```python
plt.savefig("discount_comparison_final.png", dpi=300)
```
# 실행 GIF


<img width="1394" height="858" alt="image" src="https://github.com/user-attachments/assets/13377b74-ac52-44a4-9800-bf567870a208" />

- BEST 상품 평균 할인율: 약 14%
- 일반 상품 평균 할인율: 약 5%
