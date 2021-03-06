from transitions.extensions import GraphMachine

from utils import send_text_message

import time
import datetime
from datetime import timezone
from datetime import timedelta

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_date(self, event):
        text = event.message.text
        return text == '日期'

    def is_going_to_weekday(self, event):
        text = event.message.text
        return text == '星期'

    def is_going_to_time(self, event):
        text = event.message.text
        return text == '時間'

    def is_going_to_demo(self, event):
        text = event.message.text
        return text == 'demo'

    def on_enter_date(self, event):
        send_text_message(event.reply_token, "請問您想知道西元日期或是民國日期？(輸入「西元」或「民國」)")

    def on_enter_weekday(self, event):
        send_text_message(event.reply_token, "請輸入想查詢的西元年月日(輸入「西元年/月/日」)")

    def on_enter_time(self, event):
        send_text_message(event.reply_token, "請問您想以12小時制還是24小時制表示？(輸入「12」或「24」)")

    def on_enter_demo(self, event):
        send_text_message(event.reply_token, "Now is in state demo")
        self.go_back()
        return False

    def is_going_to_date_AD(self, event):
        text = event.message.text
        return text == '西元'

    def is_going_to_date_ROC(self, event):
        text = event.message.text
        return text == '民國'

    def is_going_to_search(self, event):
        global day
        day = event.message.text
        return True

    def is_going_to_time_12(self, event):
        text = event.message.text
        return text == '12'

    def is_going_to_time_24(self, event):
        text = event.message.text
        return text == '24'

    def on_enter_date_AD(self, event):
        now = datetime.datetime.now()
        now1 = now.astimezone(timezone(timedelta(hours=+8)))
        send_text_message(event.reply_token, now1.strftime("%Y-%m-%d"))
        self.go_back()
        return False

    def on_enter_date_ROC(self, event):
        now = datetime.datetime.now()
        now1 = now.astimezone(timezone(timedelta(hours=+8)))
        result = str(now1.year-1911) + '-' + str(now1.month) + '-' + str(now1.day)
        send_text_message(event.reply_token, result)
        self.go_back()
        return False

    def on_enter_search(self, event):
        global day
        day1 = day.split('/',2)
        week_day_dict = {
            1 : '星期一',
            2 : '星期二',
            3 : '星期三',
            4 : '星期四',
            5 : '星期五',
            6 : '星期六',
            0 : '星期天',
        }
        wday = datetime.datetime(int(day1[0]),int(day1[1]),int(day1[2])).strftime("%w")
        send_text_message(event.reply_token, week_day_dict[int(wday)])
        self.go_back()
        return False

    def on_enter_time_12(self, event):
        now = datetime.datetime.now()
        now1 = now.astimezone(timezone(timedelta(hours=+8)))
        send_text_message(event.reply_token, now1.strftime("%I:%M:%S %p"))
        self.go_back()
        return False

    def on_enter_time_24(self, event):
        now = datetime.datetime.now()
        now1 = now.astimezone(timezone(timedelta(hours=+8)))
        send_text_message(event.reply_token, now1.strftime("%H:%M:%S"))
        self.go_back()
        return False

