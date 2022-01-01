import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from fsm import TocMachine
from utils import send_text_message

load_dotenv()


machine = TocMachine(
    states=["user", "date", "date_AD", "date_ROC", "weekday", "search", "time", "time_12", "time_24"],
    transitions=[
        {"trigger": "advance","source": "user","dest": "date","conditions": "is_going_to_date",},
        {"trigger": "advance","source": "user","dest": "weekday","conditions": "is_going_to_weekday",},
        {"trigger": "advance","source": "user","dest": "time","conditions": "is_going_to_time",},
        {"trigger": "advance","source": "date","dest": "date_AD","conditions": "is_going_to_date_AD",},
        {"trigger": "advance","source": "date","dest": "date_ROC","conditions": "is_going_to_date_ROC",},
        {"trigger": "advance","source": "weekday","dest": "search","conditions": "is_going_to_search",},
        {"trigger": "advance","source": "time","dest": "time_12","conditions": "is_going_to_time_12",},
        {"trigger": "advance","source": "time","dest": "time_24","conditions": "is_going_to_time_24",},
        {"trigger": "go_back", "source": ["date", "date_AD", "date_ROC", "weekday", "search", "time", "time_12", "time_24"], "dest": "user"},
    ],
    initial="user",
    auto_transitions=False,
    show_conditions=True,
)

print("2022.1.1 09.30\n");

app = Flask(__name__, static_url_path="")


# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.message.text)
        )

    return "OK"


@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        print(f"\nFSM STATE: {machine.state}")
        print(f"REQUEST BODY: \n{body}")
        response = machine.advance(event)
        #if machine.state == 'user':
        #send_text_message(event.reply_token,'請問您要使用哪項功能？\n查詢今日日期(輸入「日期」)\n查詢某日星期(輸入「星期」)\n查詢現在時間(輸入「時間」)')
        if response == False:
        	if machine.state == 'user':
        		send_text_message(event.reply_token,'請問您要使用哪項功能？\n查詢今日日期(輸入「日期」)\n查詢某日星期(輸入「星期」)\n查詢現在時間(輸入「時間」)')
    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)
