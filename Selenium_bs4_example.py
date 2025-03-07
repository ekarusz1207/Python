from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import pandas as pd

# ChromeDriver 경로 설정
chromedriver_path = r"C:\path\to\chromedriver.exe"  # ChromeDriver가 위치한 경로

# 웹 페이지 스크롤을 위해서 Selenium 사용
# Selenium 설정
chrome_options = Options()
chrome_options.add_argument("--disable-gpu") 
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
service = Service(chromedriver_path)  # ChromeDriver 경로 지정

# 브라우저 실행
driver = webdriver.Chrome(service=service, options=chrome_options)

# 페이지 요청
url = "https://www.celine.com/ko-kr/celine-%EC%97%AC%EC%84%B1/%ED%95%B8%EB%93%9C%EB%B0%B1/?nav=A003-VIEW-ALL"
driver.get(url)
time.sleep(5)  # IP 차단 방지를 위해 time.sleep으로 시간 지연

# 페이지 끝까지 스크롤
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")    # 스크롤 끝까지 내림
    time.sleep(5)   # 페이지 로딩을 위해 time.sleep으로 멈춤
    new_height = driver.execute_script("return document.body.scrollHeight")     # new_height는 스크롤을 내린 후의 페이지 높이
    if new_height == last_height:   # new_height와 last_height가 같으면 멈춤(더이상 스크롤이 내려가지 않으면 멈춤)
        break
    last_height = new_height    # 스크롤을 내린 후의 높이(new_height)를 현재 페이지의 높이(last_height) 변수에 저장

# 웹 페이지 크롤링을 위해서 BeautifulSoup 사용
# HTML 파싱
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

# 결과 처리
products = []
product_elements = soup.find_all("div", class_="m-product-listing")

for product in product_elements:
    # 상품 정보 추출
    name = product.find("div", class_="m-product-listing__meta-title f-body").text.strip() if product.find("div", class_="m-product-listing__meta-title f-body") else "정보 없음"
    price = product.find("strong", class_="f-body--em").text.strip() if product.find("strong", class_="f-body--em") else "정보 없음"
    link_tag = product.find("a", class_=False)
    link = "https://www.celine.com" + link_tag["href"] if link_tag else "정보 없음"
    image_tags = product.find_all("img", srcset=True)
    image_url = "정보 없음"
    for img in image_tags:
        srcset = img["srcset"]
        if "2000w" in srcset or "1600w" in srcset:  # srcset에서 2000w 또는 1600w 이 포함 되는 url들을 찾음
            urls = srcset.split(",")    # 찾은 url들에서 , 을 제거 후에 urls 변수에 담음
            image_url = urls[-1].strip().split(" ")[0]  # urls 변수의 맨 마지막 데이터 인덱싱 후, strip().split(" ") 으로 공백 제거 및 첫번째 데이터 인덱싱
            break

    # 상품 정보 추가
    products.append({"name": name, "price": price, "link": link, "image_url": image_url})

# 엑셀 파일로 저장하기 위해서 pandas DataFrame 및 openpyxl 사용
# 크롤링한 데이터를 pandas DataFrame으로 변환
df = pd.DataFrame(products)

# DataFrame을 엑셀 파일로 저장(vscode 설치 경로에 저장)
excel_file = "products_info.xlsx"
df.to_excel(excel_file, index=False, engine='openpyxl')

# 엑셀 파일 저장시에 출력
print(f"엑셀 파일이 저장되었습니다. : {excel_file}")

# 브라우저 종료
driver.quit()
