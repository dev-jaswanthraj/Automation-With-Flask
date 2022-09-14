import time
from app import scheduler

#@scheduler.task('interval', id="job1", seconds=5, misfire_grace_time=4)
def sendMesage() -> str:
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))


