import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from db import insert_malicious_url
from logger import logger  # logger 파일에서 가져오기
import os

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

os.makedirs('./log', exist_ok=True)

class Collector:
    def __init__(self) -> None:
        self.data_dic = dict()

    def nola_collection(self):
        """Noladefense에서 피싱 URL 수집"""

        def nola_preprocess(ent):
            """텍스트 변환: 'hxxp' -> 'http', '[.]' -> '.'"""
            text = ent.text.strip()
            return text.replace('hxxp', 'http').replace('[.]', '.')

        yesterday = datetime.now() - timedelta(days=1)
        ym = yesterday.strftime('%Y/%m')  # 연/월 (YYYY/MM)
        date = yesterday.strftime('%Y-%m-%d')  # 연-월-일 (YYYY-MM-DD)

        nola_url = f"https://www.noladefense.net/{ym}/{date}-daily-phishing-url-summary.html"

        try:
            response = requests.get(nola_url, headers=HEADERS)
            response.raise_for_status()  # HTTP 오류 발생 시 예외 발생

            soup = BeautifulSoup(response.text, 'html.parser')
            phishing_urls = [
                nola_preprocess(etr)
                for etr in soup.find_all('li')
                if etr.text.strip().startswith('hxxp')
            ]

            self.data_dic['Noladefense'] = phishing_urls
            logger.info(f"✅ Noladefense에서 {len(phishing_urls)}개의 URL 수집 완료")

        except requests.exceptions.RequestException as e:
            logger.error(f"⚠️ Noladefense 요청 실패: {e}")

    def openphish_collection(self):
        """OpenPhish에서 피싱 URL 수집"""
        openphish_url = 'https://raw.githubusercontent.com/openphish/public_feed/refs/heads/main/feed.txt'

        try:
            response = requests.get(openphish_url, headers=HEADERS)
            response.raise_for_status()  # HTTP 오류 발생 시 예외 발생

            phishing_urls = [url.strip() for url in response.text.split('\n') if url.strip()]
            self.data_dic['OpenPhish'] = phishing_urls
            logger.info(f"✅ OpenPhish에서 {len(phishing_urls)}개의 URL 수집 완료")

        except requests.exceptions.RequestException as e:
            logger.error(f"⚠️ OpenPhish 요청 실패: {e}")

    def run(self):
        """모든 수집 메서드 실행 후 결과 출력"""
        logger.info("🚀 Mal URL 수집 작업 시작")
        try:
            self.nola_collection()
            self.openphish_collection()
            logger.info("🚀 Mal URL DB Insert Start")
            for source, url_list in self.data_dic.items():
                cnt = 0
                for url in url_list:
                    status = insert_malicious_url(url, source)
                    if status:
                        cnt += 1
                
                logger.info(f"📌 저장 완료: {cnt:,} (출처: {source})")

            logger.info("✅ 모든 수집 및 저장 작업 완료")

        except Exception as e:
            logger.error(f"❌ 실행 중 오류 발생: {e}")

        finally:
            logger.info("🛑 Mal URL 수집 작업 종료")


# 실행 시 로깅
if __name__ == '__main__':
    logger.info("🔄 수집기 실행 시작")
    collector = Collector()
    collector.run()
    logger.info("🏁 수집기 실행 종료")
