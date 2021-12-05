import requests
import config

API_KEY = config.API_KEY

for page_num in range(4, 8):

    file_name_read = 'abstracts/abstracts_page' + str(page_num) + '.txt'
    # ファイルを開く
    f = open(file_name_read, 'r', encoding='UTF-8')

    # URLクエリに仕込むパラメータの辞書を作っておく
    params = {
                "auth_key": API_KEY,
                "text": f.read(),
                "source_lang": 'EN', # 入力テキストの言語を英語に設定
                "target_lang": 'JA'  # 出力テキストの言語を日本語に設定（JPではなくJAなので注意）
            }

    # パラメータと一緒にPOSTする
    request = requests.post("https://api-free.deepl.com/v2/translate", data=params) # free用のURL、有料版はURLが異なります
    result = request.json()


    file_name_write = 'abstracts_jp/abstract_page' + str(page_num) + '_jp.txt'

    # 保存
    f = open(file_name_write, 'w', encoding='UTF-8')
    f.write(result["translations"][0]["text"])
