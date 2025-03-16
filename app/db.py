import pymysql
import os
from dotenv import load_dotenv
from zlib import crc32
from logger import logger
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

def insert_malicious_url(data_dic, connection):
    commit_cnt = 0
    try:
        with connection.cursor() as cursor:
            for source, url_list in data_dic.items():
                cnt = 0  # 저장된 URL 개수

                for url in url_list:
                    url_crc = calculate_crc32(url)  # URL별로 개별 CRC32 계산

                    # 중복 확인
                    check_sql = "SELECT mal_id FROM mal_urls WHERE url_crc = %s AND url = %s"
                    cursor.execute(check_sql, (url_crc, url))
                    result = cursor.fetchone()

                    # 없을 때만 삽입
                    if result is None:
                        insert_sql = "INSERT INTO mal_urls (url, url_crc, source) VALUES (%s, %s, %s)"
                        cursor.execute(insert_sql, (url, url_crc, source))
                        commit_cnt += 1
                        cnt += 1  # 저장된 URL 개수 증가

                    # 100개 단위로 커밋
                    if commit_cnt % 100 == 0:
                        connection.commit()

                logger.info(f"📌 저장 완료: {cnt:,} (출처: {source})")

        connection.commit()  # 마지막 남은 데이터 커밋
    except Exception as e:
        logger.error(f"❌ DB 저장 중 오류 발생: {e}")
        connection.rollback()  # 오류 발생 시 롤백