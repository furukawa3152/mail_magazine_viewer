import os
import json
import re
import gspread
import time
import requests
from openai import OpenAI
from google.oauth2.service_account import Credentials
from datetime import datetime
chat_GPT_API_key = os.environ["API_KEY"]
def make_notes(columnA,columnB):
    scope = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive']
    #ダウンロードしたjsonファイル名をクレデンシャル変数に設定。
    credentials = Credentials.from_service_account_file("my-project-20230927-1db60d7e8989.json", scopes=scope)

    gc = gspread.authorize(credentials)

    #スプレッドシートIDを変数に格納する。
    SPREADSHEET_KEY = '1wjS_kDyKMi65DHWCaHNWeLLFyslr5DL8NEyLRTEhPXI'
    # スプレッドシート（ブック）を開く
    workbook = gc.open_by_key(SPREADSHEET_KEY)
    worksheet = workbook.worksheet("シート1")
    # 追記したいデータ（A列のデータ、B列のデータ）
    new_data_a = columnA
    new_data_b = columnB
    today_str = datetime.now().strftime('%Y-%m-%d')
    # A列B列に同時にデータを追加する
    worksheet.append_row([new_data_a, new_data_b,today_str])

def read_textdata():
    scope = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive']
    #ダウンロードしたjsonファイル名をクレデンシャル変数に設定。
    credentials = Credentials.from_service_account_file("my-project-20230927-1db60d7e8989.json", scopes=scope)

    gc = gspread.authorize(credentials)

    #スプレッドシートIDを変数に格納する。
    SPREADSHEET_KEY = '1wjS_kDyKMi65DHWCaHNWeLLFyslr5DL8NEyLRTEhPXI'
    # スプレッドシート（ブック）を開く
    workbook = gc.open_by_key(SPREADSHEET_KEY)
    worksheet = workbook.worksheet("data")
    a1_value = worksheet.acell('A1').value
    return a1_value
def chat_gpt_return(input_data):
    client = OpenAI(api_key=chat_GPT_API_key)
    chat_completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system",
                   "content": "以下に与えるメールマガジンの文章を、内容ごとに分割して出力して下さい。改行してあっても同一のトピックである場合もあるので、精査して同一の内容の場合は一つのvalueにすること。分割した文章には日本語で内容を要約した簡潔な見出しをつけ、見出しをkeyに、内容をvalueに持つjson形式にしてください。keyは必ず日本語です。valueの部分は絶対に要約せず、原文のままで出力すること。質問、回答形式になっている部分については、質問と回答をセットにして一つのvalueとして扱ってください。その際のkeyは質問内容の要約とし、頭に「質問コーナー：」とつけて下さい。質問内容、回答は要約せず原文のままで書き出すこと。回答のまえには改行を入れて下さい。jsonについては{'key1':'value1','key2':'value2'}という1層構造にし、これ以上ネストすることは固く禁止します。必ずjsonのみを出力すること。"},
                  {"role": "user", "content": input_data}],
        temperature=0.2,
    )
    return (chat_completion.choices[0].message.content,chat_completion.usage)


if __name__ == '__main__':
    data = (read_textdata())
    # json_data = '''
    # {
    #     "key1": "value1",
    #     "key2": "value2",
    #     "key3": "value3"
    # }
    # '''

    return_text,usage = chat_gpt_return(data)
    print(return_text,usage)

    start_index = return_text.find('{')
    end_index = return_text.rfind('}') + 1
    json_text = return_text[start_index:end_index]
    # テキスト内の制御文字を正規表現で削除する
    json_text_replaced = re.sub(r'[\x00-\x1F\x7F]', '', json_text)
    # JSON文字列をPythonの辞書に変換
    try:
        json_data = json.loads(json_text_replaced)
        print("JSON部分のデータ:")
        print(json_data)
    except json.JSONDecodeError as e:
        print(f"JSONデータの解析に失敗しました: {e}")
    dict_data = json.loads(json_text_replaced)
    for key,value in dict_data.items():
        make_notes(key,value)
        time.sleep(2)


