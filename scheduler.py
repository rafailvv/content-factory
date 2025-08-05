from apscheduler.executors.asyncio import AsyncIOExecutor
from apscheduler.schedulers.asyncio import AsyncIOScheduler


class PostScheduler:
    def __init__(self, send, cfg):
        self.send = send
        self.scheduler = AsyncIOScheduler(
            timezone="UTC",
            executers = {'default' : AsyncIOExecutor()}
        )
        self.cfg = cfg
        self.times = cfg.post_schedule_utc

    def start(self):
        for t in self.times:
            h, m = map(int, t.split(":"))
            self.scheduler.add_job(
                self.send, 'cron', args=[self.cfg], hour=h, minute=m
            )
            print(f"Задача добавлена для {h}:{m}")
        self.scheduler.start()