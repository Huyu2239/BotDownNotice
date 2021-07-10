# BotDownNotice
Botがダウンし反応しない場合に、指定したチャンネルに開発者へのメンションを送信します。
# 使い方
config.json に必要な情報を書き込み、main.pyを起動させてください。  
## BotName(str)
起動させるBotの名前
## TOKEN(str)
起動させるBotのTOKEN
## commands(list(str))
発火されたときに、そのチャンネルにBotから必ずメッセージが送信されるコマンド
## log_ch_id(int)
通知を送信するチャンネルのID
## down_msg(str)
利用者に送信するメッセージ
## notice_msg(str)
送信する通知内容
## mention_span(int)
メンションの感覚を指定  
0の場合は一度のみ送信