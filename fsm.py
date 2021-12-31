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
        #flag = (text == "日期")
        #if flag == False:
            #self.go_back(event)
        return text == '日期'

    def is_going_to_weekday(self, event):
        text = event.message.text
        #flag = (text == "星期")
        #if flag == False:
            #self.go_back(event)
        return text == '星期'

    def is_going_to_time(self, event):
        text = event.message.text
        #flag = (text == "時間")
        #if flag == False:
            #self.go_back(event)
        return text == '時間'

    def on_enter_date(self, event):
        send_text_message(event.reply_token, "請問您想知道西元日期或是民國日期？(輸入「西元」或「民國」)")

    def on_enter_weekday(self, event):
        send_text_message(event.reply_token, "請輸入想查詢的西元年月日(輸入「西元年/月/日」)")

    def on_enter_time(self, event):
        send_text_message(event.reply_token, "請問您想以12小時制還是24小時制表示？(輸入「12」或「24」)")

    def is_going_to_date_AD(self, event):
        text = event.message.text
        #flag = (text == "西元")
        #if flag == False:
            #self.go_back(event)
        return text == '西元'

    def is_going_to_date_ROC(self, event):
        text = event.message.text
        #flag = (text == "民國")
        #if flag == False:
            #self.go_back(event)
        return text == '民國'

    def is_going_to_search(self, event):
        global day
        day = event.message.text
        return True

    def is_going_to_time_12(self, event):
        text = event.message.text
        #flag = (text == "12")
        #if flag == False:
            #self.go_back(event)
        return text == '12'

    def is_going_to_time_24(self, event):
        text = event.message.text
        #flag = (text == "24")
        #if flag == False:
            #self.go_back(event)
        return text == '24'

    def on_enter_date_AD(self, event):
        now = datetime.datetime.now()
        now1 = now.astimezone(timezone(timedelta(hours=+8)))
        #result = time.strftime("%Y-%m-%d", now)
        send_text_message(event.reply_token, now1.strftime("%Y-%m-%d"))
        self.go_back()

    def on_enter_date_ROC(self, event):
        now = datetime.datetime.now()
        now1 = now.astimezone(timezone(timedelta(hours=+8)))
        result = str(now1.year-1911) + '-' + str(now1.month) + '-' + str(now1.day)
        send_text_message(event.reply_token, result)
        self.go_back()

    def on_enter_search(self, event):
        global day
        day1 = day.split('/')
        week_day_dict = {
            0 : '星期一',
            1 : '星期二',
            2 : '星期三',
            3 : '星期四',
            4 : '星期五',
            5 : '星期六',
            6 : '星期天',
        }
        wday = datetime.datetime(day1[0],day[1],day[2]).strftime("%w")
        send_text_message(event.reply_token, week_day_dict[wday])
        self.go_back()

    def on_enter_time_12(self, event):
        now = datetime.datetime.now()
        now1 = now.astimezone(timezone(timedelta(hours=+8)))
        #result = time.strftime("%I:%M:%S %p", now)
        send_text_message(event.reply_token, now1.strftime("%I:%M:%S %p"))
        self.go_back()

    def on_enter_time_24(self, event):
        now = datetime.datetime.now()
        now1 = now.astimezone(timezone(timedelta(hours=+8)))
        #result = time.strftime("%H:%M:%S", now)
        send_text_message(event.reply_token, now1.strftime("%H:%M:%S"))
        self.go_back()

