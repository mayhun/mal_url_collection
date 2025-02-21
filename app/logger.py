import logging
from datetime import datetime

def setup_logger():
    """로거 설정 함수"""
    date = datetime.now().strftime('%Y%m%d')
    logger = logging.getLogger("MaliciousURLCollector")
    logger.setLevel(logging.INFO)

    # 파일 핸들러 (collector.log 파일에 기록)
    file_handler = logging.FileHandler(f"./log/Collection_{date}.log", encoding="utf-8")
    file_handler.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # 로그 포맷 지정
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # 핸들러 추가
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

# 전역 로거 객체
logger = setup_logger()
