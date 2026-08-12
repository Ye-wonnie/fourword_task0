"""
임시 검증용 서버
- 실제 데이터 수집/DB 저장 로직은 없음
- 목적: (1) 핑이 서버를 깨우는지 (2) 스케줄러가 정해진 시간에 도는지 확인용
"""

from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI()

# 서버 시작 시각 (슬립 후 재시작되면 이 값이 바뀜 -> 슬립 여부 확인 가능)
SERVER_START_TIME = datetime.now()


# ------------------------------------------------------------
# 1. 핑 확인용 엔드포인트
#    GitHub Actions가 이 주소로 주기적으로 요청을 보냄
# ------------------------------------------------------------
@app.get("/")
def health_check():
    now = datetime.now()
    logger.info(f"[PING] 서버 살아있음 확인 요청 도착 - {now}")
    return {
        "status": "alive",
        "server_start_time": SERVER_START_TIME.isoformat(),
        "current_time": now.isoformat(),
    }


# ------------------------------------------------------------
# 2. 스케줄러 - 실제 배포에서는 "1일 1회" 이지만,
#    지금은 검증을 빨리 하기 위해 "1분마다" 로 임시 설정.
#    -> 실제 완성 서버에서는 아래 trigger 부분만
#       trigger='cron', hour=3 (원하는 시각) 으로 바꾸면 됨
# ------------------------------------------------------------
def scheduled_job():
    now = datetime.now()
    logger.info(f"[SCHEDULER] 데이터 수집 작업 실행됨 - {now}")
    # TODO: 실제 데이터 수집 + Supabase 저장 로직은 여기에 나중에 추가


scheduler = BackgroundScheduler()

# 검증용: 1분마다 실행 (원래는 하루 1회 -> 나중에 cron으로 교체)
scheduler.add_job(scheduled_job, "interval", minutes=1, id="collect_job")

scheduler.start()

logger.info("서버 시작됨. 스케줄러도 함께 시작됨.")
