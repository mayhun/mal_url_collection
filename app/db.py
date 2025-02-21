import pymysql
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='../config/.env.local')

# DB 연결 설정 (환경 변수에서 불러오기)
HOST = os.getenv('DB_HOST')
USER = os.getenv('DB_USER')
PW = os.getenv('DB_PASSWORD')
DB = os.getenv('DB_NAME')
PORT = int(os.getenv('DB_PORT'))

# DB 연결 생성
connection = pymysql.connect(
    host=HOST,
    user=USER,
    password=PW,
    database=DB,
    port=PORT,
    cursorclass=pymysql.cursors.DictCursor
)


def insert_malicious_url(url, source):
    try:
        with connection.cursor() as cursor:
            # 중복 확인
            check_sql = "SELECT mal_id FROM mal_urls WHERE url = %s"
            cursor.execute(check_sql, (url,))
            result = cursor.fetchone()

            # 없을 때만 삽입
            if result is None:
                insert_sql = "INSERT INTO mal_urls (url, source) VALUES (%s, %s)"
                cursor.execute(insert_sql, (url, source))
                connection.commit()
                
                return True

            else:
                return False
        
    except Exception as e:
        print(f"Error: {e}")
        return False
    
