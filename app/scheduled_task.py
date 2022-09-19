import time
from app import scheduler
from .models import W2Form
import app

#@scheduler.task('interval', id="job1", seconds=10, misfire_grace_time=4)
def sendMesage():
    t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    try:
        ctx = app.app.app_context()
        ctx.push()
        forms = W2Form.query.all()
        with open('dblog.txt', 'w') as f:
            for form in forms:
                f.write(f'{form.id}, {form.emp_social_num}, {form.ein}, {form.emp_address}, {form.control_num}\n')
            f.close()
        ctx.pop()
        print("Done")
    except:
        print(t)


