# -*- coding: utf-8 -*-

# Convert chat to xml ver1.0.2
# Convert youtube chat json to niconicko comment xml.
# YouTube のチャットファイル(.live_chat.json)をニコニコ動画のxml形式に変換する関数
# チャットファイルはyoutube-dlやyt-dlpなどでダウンロードしたものの形式で動きます。
# YouTube のチャットファイルプレイヤーが見つからなかったので、似た機能であるニコニコ動画プレイヤーでチャットを再生できるように変換する関数です。
# ニコニコ動画コメントプレイヤーには commeon などを利用してください。

# ■ 使い方
# コマンドプロンプトで、下記のように実行します。
# 渡されたパスがフォルダーの場合は、フォルダー内のjsonを一括処理します。
# 変換されたxmlファイルは、「xml」フォルダー内に保存されます。
#
# python "C:\Users\<USER_NAME>\Desktop\test\convert_chat_to_xml.py" "C:\Users\<USER_NAME>\Desktop\test\_video\20190530 - #05【悪魔城ドラキュラ】諦めない心ッ…！！鈴原るるは戦う！【鈴原るる_にじさんじ】 - [Sbh6TXCxs40].live_chat.json"

import datetime, json, sys , os, datetime, re

# 変換したいjsonのファイルパス
target_dir = sys.argv[1]


# jsonファイルの読み込み
def import_json(target_dir):
    path = target_dir
    json_open = open(path, 'r',encoding="utf-8")
    json_load = []
    decoder = json.JSONDecoder()
    with json_open as f:
        line = f.readline()
        while line:
            json_load.append(decoder.raw_decode(line))
            line = f.readline()
    return json_load

# タイムスタンプが0:00のようになっているので、全て秒に変換
def convert_timetext(time_text, user_name, text):
    time_l = time_text.split(":")
    if len(time_l) == 2:
        mini, sec = time_l
        hour = 0
    elif len(time_l) == 3:
        hour, mini, sec = time_l
    try:
        second = (int(hour) * 3600) + (int(mini) * 60) + (int(sec))
    except ValueError:
        print("ValueError  > %s「%s」" % (user_name,text))
        return "0"
    time_text = str(second) + "00"
    return time_text


# テキスト内の特殊文字を変換
def replace_text(text):
    text = text.replace("<", "&lt;")	# 小なりの記号。タグを表記したいときにも必要
    text = text.replace(">", "&gt;")	# 大なりの記号。タグを表記したいときにも必要
    text = text.replace("&", "&amp;")	# アンパサンド。実体参照で使うため、記号として表示するときに必要
    text = text.replace(" ", " ")	# ノーブレークスペース
    text = text.replace(" ", " ")	# フォントサイズの半分のスペース
    text = text.replace(" ", " ")	# フォントサイズのスペース
    text = text.replace("–", "-")	# フォントサイズ半分のダッシュ
    text = text.replace("—", "-")	# フォントサイズのダッシュ
    text = text.replace("'","&#039;")
    return text

# さんぷる
# <chat thread="1640883302" no="1" vpos="704" date="1000000012" date_usec="2" anonymity="1" user_id="hR1wp4m-xxIaU2RgsVMr4zPyzeU" mail="184" leaf="0" premium="1" score="0">うぽつですー</chat>


# コア関数
def convert_youtube_chat_json_to_nico_xml(target_dir):
    info_start_time = datetime.datetime.now()

    if os.path.isfile(target_dir):
        path_l = [target_dir]
    else:
        path_l = [os.path.join(target_dir,i) for i in os.listdir(target_dir)]

    for index,target_path in enumerate(path_l):
        # if index == 0:
        #     print("Create 'xml' Folder")
        #     os.makedirs(os.path.join(os.path.dirname(target_path),"xml"), exist_ok=True)
        if not os.path.splitext(target_path)[1] == ".json":
            continue
        print("file_name",target_path)

        print("==================================")
        print("===> Run > %s" % os.path.basename(target_path))
        print("===> Start Import json")
        json_load = import_json(target_path)
        print("===> Start convert")
        # jsonの必要な情報を整形
        line_l = ["<packet>\n"]
        finished_l = []
        for index, item in enumerate(json_load):
            if not "addChatItemAction" in item[0]['replayChatItemAction']['actions'][0].keys():
                continue
            if not "liveChatTextMessageRenderer" in item[0]['replayChatItemAction']['actions'][0]['addChatItemAction']['item'].keys():
                continue
            render = item[0]['replayChatItemAction']['actions'][0]['addChatItemAction']['item']['liveChatTextMessageRenderer']
            #
            # ユーザーネーム
            if "authorName" in render.keys():
                user_name = render['authorName']['simpleText']
            else:
                user_name = ""
            #
            # テキストを整形(絵文字は別の模様。ここはまだ調整必要)
            text = ""
            if "text" in render['message']['runs'][0].keys():
                text = render['message']['runs'][0]['text']
            if len(render['message']['runs'][0]) >= 2:
                text += render['message']['runs'][1]['emoji']
            #
            # タイムスタンプ
            time_text = render['timestampText']['simpleText']
            time_text = convert_timetext(time_text, user_name, text)
            line_l += ["<chat vpos='%s' no='%s' user_id='%s'> %s </chat>\n" % (time_text, index , replace_text(user_name), replace_text(text))]
            finished_l += [1]
        #
        print("===> Finished items [%s]" % str(len(finished_l)))
        #
        # ファイルに書き込み
        print("===> Start write xml")
        line_l += ["</packet>"]
        new_path = target_path.replace(".live_chat.json","") + ".xml"
        new_path = os.path.join(os.path.dirname(new_path),os.path.basename(new_path))
        with open(new_path, mode='w',encoding="utf-8") as f:
            f.writelines(line_l)

        date_o = datetime.datetime.now() - info_start_time
        date_o_l = re.match("^(.+\.)(\d\d)\d\d\d\d$",str(date_o))
        date_o = date_o_l[1] + date_o_l[2]
        print("\n===> __Saved__ [%s]> %s\n\n\n" % (date_o,new_path))

    date_o = datetime.datetime.now() - info_start_time
    date_o_l = re.match("^(.+\.)(\d\d)\d\d\d\d$",str(date_o))
    date_o = date_o_l[1] + date_o_l[2]
    print("All Finished [%s]" % date_o)


# 実行
if __name__ == "__main__":
    convert_youtube_chat_json_to_nico_xml(target_dir)
