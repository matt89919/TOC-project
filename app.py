import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from fsm import TocMachine
from utils import *

load_dotenv()


machine = TocMachine(
    states=["start", "menu", "intro", "helpermenu", "input", "web", "mode1", "mode2", "mode3",
            "roast", "method", "country", "l", "m", "d", "washed", "natural", "honey", "africa", "asia", "ca",
            "aftercountry","afterhelper", "premode"],
    transitions=[
        {
            "trigger": "advance",
            "source": "start",
            "dest": "menu",
            "conditions": "start_to_menu",
        },
        {
            "trigger": "advance",
            "source": "menu",
            "dest": "intro",
            "conditions": "menu_to_intro",
        },
        {
            "trigger": "advance",
            "source": "intro",
            "dest": "roast",
            "conditions": "intro_to_roast",
        },
        {
            "trigger": "advance",
            "source": "roast",
            "dest": "l",
            "conditions": "roast_to_l",
        },
        {
            "trigger": "advance",
            "source": "roast",
            "dest": "m",
            "conditions": "roast_to_m",
        },
        {
            "trigger": "advance",
            "source": "roast",
            "dest": "d",
            "conditions": "roast_to_d",
        },
        {
            "trigger": "advance",
            "source": "intro",
            "dest": "method",
            "conditions": "intro_to_method",  
        },
        {
            "trigger": "advance",
            "source": "method",
            "dest": "washed",
            "conditions": "method_to_washed",  
        },
        {
            "trigger": "advance",
            "source": "method",
            "dest": "honey",
            "conditions": "method_to_honey",  
        },
        {
            "trigger": "advance",
            "source": "method",
            "dest": "natural",
            "conditions": "method_to_natural",  
        },
        {
            "trigger": "advance",
            "source": "intro",
            "dest": "country",
            "conditions": "intro_to_country",   
        },
        {
            "trigger": "advance",
            "source": "country",
            "dest": "asia",
            "conditions": "country_to_asia",   
        },
        {
            "trigger": "advance",
            "source": "country",
            "dest": "africa",
            "conditions": "country_to_africa",   
        },
        {
            "trigger": "advance",
            "source": "country",
            "dest": "ca",
            "conditions": "country_to_ca",   
        },
        {
            "trigger": "go_back",
            "source": ["africa","asia","ca", "l", "m", "d", "washed", "natural", "honey"],
            "dest": "aftercountry", 
        },
        {
            "trigger": "advance",
            "source": "aftercountry",
            "dest": "premode",
            "conditions": "after_to_helper",   
        },
        {
            "trigger": "advance",
            "source": "aftercountry",
            "dest": "intro",
            "conditions": "after_to_intro",   
        },
        {
            "trigger": "advance",
            "source": "aftercountry",
            "dest": "menu",
            "conditions": "after_to_menu",   
        },
        {
            "trigger": "advance",
            "source": "menu",
            "dest": "premode",
            "conditions": "menu_to_helpermenu",
        },
        {
            "trigger": "advance",
            "source": "premode",
            "dest": "helpermenu",
            "conditions": "premode_to_helpermenu",
        },
        {
            "trigger": "advance",
            "source": "helpermenu",
            "dest": "mode1",
            "conditions": "helpermenu_to_mode1",
        },
        {
            "trigger": "advance",
            "source": "helpermenu",
            "dest": "mode2",
            "conditions": "helpermenu_to_mode2",
        },
        {
            "trigger": "advance",
            "source": "helpermenu",
            "dest": "mode3",
            "conditions": "helpermenu_to_mode3",  
        },
        {
            "trigger": "advance",
            "source": "menu",
            "dest": "input",
            "conditions": "menu_to_input",
        },
        {
            "trigger": "advance",
            "source": "input",
            "dest": "web",
            "conditions": "input_to_web",
        },
        {
            "trigger": "advance",
            "source": "premode",
            "dest": "menu",
            "conditions": "backto_menu",
        },
        {
            "trigger": "advance",
            "source": "afterhelper",
            "dest": "intro",
            "conditions": "afterhelper_to_intro",
        },
        {
            "trigger": "advance",
            "source": "afterhelper",
            "dest": "input",
            "conditions": "afterhelper_to_web",
        },
        {
            "trigger": "advance",
            "source": "afterhelper",
            "dest": "menu",
            "conditions": "afterhelper_to_menu",
        },
        {
            "trigger": "go_back", 
            "source": "web", 
            "dest": "menu", 
        },
        {
            "trigger": "go_back", 
            "source": ["mode1", "mode2", "mode3"], 
            "dest": "afterhelper", 
        },
        {
            "trigger": "advance", 
            "source": ["country", "method", "roast"], 
            "dest": "intro",   
            "conditions":"backto_intro"
        },
        {
            "trigger": "advance", 
            "source": ["intro", "input", "helpermenu"], 
            "dest": "menu",   
            "conditions":"backto_menu"
        },
        
    ],
    initial="start",
    auto_transitions=False,
    show_conditions=True,
)

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
        if response == False:
            send_text_message(event.reply_token, "Not Entering any State")

    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)