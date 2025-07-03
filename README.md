# Pulmuone Scraper
이 프로젝트는 Python Selenium을 이용해서
**풀무원 쇼핑몰의 상품 데이터를 자동으로 수집** 하고,
그 결과를 **엑셀 파일로 저장하는 프로그램** 입니다.

-----

# 사용 기술
- 개발 환경
    - Python
- 주요 라이브러리
    - Selenium (웹페이지 자동화)
    - pandas
- 개발 환경 
    - Pycharm
- 활용 드라이버
  - chromeDriver

# 사용 방법
Pulmuone Scraper를 사용하기 위한 방법을 나열합니다.

사용 방법은 IDE(Pycharm)를 통한 방법과 CMD에서 실행하는 2가지 방법이 있습니다.

## 사전 설치 항목 
1. Python 설치
   - Link: https://www.python.org/downloads/

3. ChromeDriver 설치
   - Link: ~~~~

5. Pycharm 설치(Option)
   - Link: ~~~~

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
1. Git pull
```bash
git clone https://github.com/jeongwonleeee/PHI_Project1.git
```

2. Python 파일 실행
```bash
cd PHI_Project1
python3 main.py
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

# 실행 GIF
