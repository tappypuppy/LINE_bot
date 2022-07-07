from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os

app = Flask(__name__)

#get env
YOUR_CHANNEL_ACCESS_TOKEN = "zxo1pWHwhlq3KxuHX4NOO83R1t31Zguj6kvRo5dU5/uyrO1T5JAkUVu/t3y80NryyEOM0bVMJSMC0ibZUNj3gi+6o157qd39Q6XNQxYhgoVac4cih0uHgSSbAdTiYai0N6aUr4hImpcLP77wh8679QdB04t89/1O/w1cDnyilFU="
YOUR_CHANNEL_SECRET = "abd382a39d5fdefd4420befd1de0d369"
line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]

    body=request.get_data(as_text=True)
    app.logger.info("Request body" + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    mentionId = event.message.mentionees[0].userId
    if mentionId == "オウム返しボット":
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="unko"))
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=event.message.text))

if __name__ =="__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)