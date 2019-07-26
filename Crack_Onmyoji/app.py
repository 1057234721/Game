from flask import Flask, render_template, request, redirect, session, url_for
import re
import sys
import time
from Crack_Onmyoji.log_recorder import LogRecorder
from Crack_Onmyoji.crack_onmyoji import Cracker

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'GET':
        return render_template('task.html')
    else:
        task0 = request.form.get('player0')
        task1 = request.form.get('player1')
        task2 = request.form.get('player2')
        task3 = request.form.get('player3')
        arg0 = request.form.get('arg0')
        arg1 = request.form.get('arg1')
        arg2 = request.form.get('arg2')
        arg3 = request.form.get('arg3')
        print(task0, task1, task2, task3)
        print(arg0, arg1, arg2, arg3)
        if task0 != '':
            if arg0 != '':
                c0 = Cracker(0, [[task0, arg0]])
            else:
                c0 = Cracker(0, [[task0]])
            c0.start()
        if task1 != '':
            if arg1 != '':
                c1 = Cracker(1, [[task1, arg1]])
            else:
                c1 = Cracker(1, [[task1]])
            c1.start()
        if task2 != '':
            if arg2 != '':
                c2 = Cracker(2, [[task2, arg2]])
            else:
                c2 = Cracker(2, [[task2]])
            c2.start()
        if task3 != '':
            if arg3 != '':
                c3 = Cracker(3, [[task3, arg3]])
            else:
                c3 = Cracker(3, [[task3]])
            c3.start()
        return render_template('detail.html', count='223')


if __name__ == '__main__':
    run_time = time.strftime("%Y %m %d %H:%M:%S", time.localtime())
    sys.stdout = LogRecorder('./logs/' + '_'.join(re.split(r'[\\ |:]', run_time)) + '_log.txt')
    app.run(debug=True)
