import pymysql
import os
from dotenv import load_dotenv
from zlib import crc32

load_dotenv(dotenv_path='../config/.env')

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

def calculate_crc32(url):
    return crc32(url.encode()) & 0xffffffff

def insert_malicious_url(url, source):
    try:
        with connection.cursor() as cursor:
            url_crc = calculate_crc32(url)

            # 중복 확인
            check_sql = "SELECT mal_id FROM mal_urls WHERE url_crc = %s AND url = %s"
            cursor.execute(check_sql, (url_crc, url))
            result = cursor.fetchone()

            # 없을 때만 삽입
            if result is None:
                insert_sql = "INSERT INTO mal_urls (url, url_crc, source) VALUES (%s, %s, %s)"
                cursor.execute(insert_sql, (url, url_crc, source))
                connection.commit()
                return True
            else:
                return False
    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        connection.close()