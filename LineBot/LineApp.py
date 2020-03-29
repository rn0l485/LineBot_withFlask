from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *
from jsonList import introduce, information, Tickets, welcome

# Channel Access Token
line_bot_api = LineBotApi('Channel Access Token Here')
# Channel Secret
handler = WebhookHandler('Channel Secret Here')

app = Flask(__name__)


# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    sendText = event.message.text
    if sendText == '簡介/Introduce':
        message = FlexSendMessage(alt_text='Etron Intro', contents=introduce)
    elif sendText == '疑問/Help':
        message = TextSendMessage(text='請手動加入宜昌自動化有限公司LINE好友\nid帳號：H86428377\n我們的客服將為您服務。')
        # TODO, put the contact account here
    elif sendText == '聯絡窗口設定/Setting' : 
        message = FlexSendMessage(alt_text='Info Setting', contents=information)
    elif sendText == '商品選擇表/Ticket' :
        message = FlexSendMessage(alt_text='Ticket', contents=Tickets)
    else:
        message = FlexSendMessage(alt_text='welcome', contents=welcome)

    line_bot_api.reply_message(event.reply_token, message)
    #message = TextSendMessage(text=event.message.text)
    #line_bot_api.reply_message(event.reply_token, message)

@handler.add(FollowEvent)
def handle_message(event):
    message = FlexSendMessage(alt_text='welcome', contents=welcome)
    line_bot_api.reply_message(event.reply_token, message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, threaded=True)
















