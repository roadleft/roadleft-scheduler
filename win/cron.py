from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.schedulers.background import BackgroundScheduler
import asyncio
import webbrowser

executors = {
    'default': ThreadPoolExecutor(20)
}


def open_note():
        webbrowser.open("http://127.0.0.1:8000/", 1)

scheduler = BackgroundScheduler(executors=executors, daemon=True)
scheduler.add_job(open_note, 'cron', day_of_week='*', hour='9-17', minute='0', second='0')
scheduler.start()
loop = asyncio.get_event_loop()

loop.run_forever()