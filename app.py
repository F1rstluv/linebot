import os
import sys
from flask import Flask, request, abort

from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration, ApiClient, MessagingApi,
    ReplyMessageRequest, TextMessage
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent

app = Flask(__name__)

# ตรวจสอบตัวแปรสภาพแวดล้อมก่อนเริ่มทำงาน
channel_secret = os.environ.get("LINE_CHANNEL_SECRET")
channel_access_token = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")

if not channel_secret or not channel_access_token:
    print("Error: โปรดตั้งค่า LINE_CHANNEL_SECRET และ LINE_CHANNEL_ACCESS_TOKEN")
    sys.exit(1)

handler = WebhookHandler(channel_secret)
config = Configuration(access_token=channel_access_token)

# สร้าง Instance ของ ApiClient และ MessagingApi ไว้ภายนอกเพื่อนำกลับมาใช้ซ้ำได้
api_client = ApiClient(config)
line_bot_api = MessagingApi(api_client)

@app.route("/")
def home():
    return "LINE Webhook is running"

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK"

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    line_bot_api.reply_message(
        ReplyMessageRequest(
            reply_token=event.reply_token,
            messages=[
                TextMessage(
                    text="สวัสดีครับ LINE Bot ทำงานแล้ว"
                )
            ]
        )
    )

if __name__ == "__main__":
    app.run(port=5000)