import pandas as pd
import pymysql

# 엑셀 데이터 불러오기
df = pd.read_excel("C:/Users/pa/PyCharmMiscProject/pulmuone_products_with_tag.xlsx")

# DB 연결
conn = pymysql.connect(
    host='localhost',
    user='<your_database_username>,
    password='<your_database_password>',
    db='<<your_database>',
    charset='utf8mb4',
    autocommit=True
)
cursor = conn.cursor()

# 데이터 삽입 (컬럼 이름은 네 테이블에 맞게 수정)
for i, row in df.iterrows():
    sql = """
    INSERT INTO `pulmuone-products` (name, price, discount_rate, tag)
    VALUES (%s, %s, %s, %s)
    """
    cursor.execute(sql, (
        row['상품명'],
        int(str(row['가격']).replace(',', '')),  # ← 쉼표 제거 후 숫자로 변환!
        str(row['할인율']),
        str(row['태그'])
    ))

cursor.close()
conn.close()
print("✅ 데이터 삽입 완료!")