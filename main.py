# 본 코드는 공공데이터 포털(https://www.data.go.kr)에서 제공하는 
# "식품의약품안전처_화장품 원료성분정보" API를 활용하여 작성되었습니다.
# 이용허락범위: 제한 없음 (공공데이터의 제공 및 이용 활성화에 관한 법률)
# 라이선스: MIT License

import os
import json
import requests
from dotenv import load_dotenv
from datetime import datetime

# .env 파일에서 환경 변수 로드
load_dotenv()

def get_cosmetic_ingredients(ingredient_name, page_no=1, num_of_rows=10):
    # 인코딩된 API 키 사용
    api_key = os.getenv('PUBLIC_DATA_API_KEY_ENCODING')
    
    url = "http://apis.data.go.kr/1471000/CsmtcsIngdCpntInfoService01/getCsmtcsIngdCpntInfoService01"
    params = {
        'serviceKey': api_key,
        'type': 'json',
        'INGR_KOR_NAME': ingredient_name,
        'pageNo': str(page_no),
        'numOfRows': str(num_of_rows)
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

def save_to_json(data, ingredient_name):
    # 현재 날짜와 시간을 파일명에 포함
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"cosmetic_ingredient_{ingredient_name}_{current_time}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    print(f"Data saved to {filename}")

def main():
    ingredient_name = input("검색할 화장품 원료 이름을 입력하세요: ")
    page_no = 1
    num_of_rows = 10
    total_count = 0

    while True:
        result = get_cosmetic_ingredients(ingredient_name, page_no, num_of_rows)
        
        if result and 'body' in result:
            items = result['body'].get('items', [])
            if items:
                save_to_json(items, ingredient_name)
                
                total_count += len(items)
                print(f"페이지 {page_no} 데이터 저장 완료. 총 {total_count}개의 항목 저장됨.")
                
                if total_count >= result['body'].get('totalCount', 0) or total_count >= 10000:
                    print("모든 데이터를 가져왔거나 트래픽 제한에 도달했습니다.")
                    break
                
                page_no += 1
            else:
                print("더 이상 데이터가 없습니다.")
                break
        else:
            print("데이터를 가져오는데 실패했습니다.")
            break

if __name__ == "__main__":
    main()