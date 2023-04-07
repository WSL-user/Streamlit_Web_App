import requests
import openai
import streamlit as st
import random

URL = 'http://webservice.recruit.co.jp/hotpepper/gourmet/v1/'
#API_KEYは外部に漏らさないで(おなげえしやす)
#TODO　自分のAPIキーに変更してください

API_KEY = 'YOUR HOTPEPPER API KEY'
openai.api_key='YOUR CHATGPT API KEY'
model_engine = "text-davinci-003"


#宣伝文を作る関数
def make_propaganda(prompt):
    '''
    This function gets the user input, pass it to ChatGPT function and 
    displays the response
    '''
    # Get user input
    if prompt != ":q" or prompt != "":
        # Pass the query to the ChatGPT function
        response = ChatGPT(prompt)
        return response
        #return st.write(f"{user_query} {response}")

#chatGPTを呼ぶ関数
def ChatGPT(user_query):
    ''' 
    This function uses the OpenAI API to generate a response to the given 
    user_query using the ChatGPT model
    '''
    # Use the OpenAI API to generate a response
    completion = openai.Completion.create(
                                  engine = model_engine,
                                  prompt = user_query,
                                  max_tokens = 1024,
                                  n = 1,
                                  temperature = 0.5,
                                      )
    response = completion.choices[0].text
    return response

#ホットペッパーグルメから情報を得る関数
def ask_hotpepper(keyword, count=100):
    #https://webservice.recruit.co.jp/doc/hotpepper/reference.htmlを参照
    body = {
      'key':API_KEY,
      'keyword': keyword, #
      'format':'json',
      'count':count,
      'type':"special"
    }
    response = requests.get(URL,body)
    return response

#ホットペッパーグルメのレスポンスからChatGPTに聞くプロンプトをテンプレートベースで生成する関数
def make_prompt_list(response):
    prompts = {}

    for shop in response.json()['results']['shop']:
        shop_name = shop["name"]
        genre_name = shop["genre"]["name"]
        catch = shop["genre"]["catch"]

        prompt = f"""
          次の特徴を踏まえて、飲食店の400文字程度の宣伝文を生成してください。なお、「:」の前側の言葉は使用しないでください
          店名: {shop_name}
          ジャンル: {genre_name}
          キャッチフレーズ: {catch}"""

        for key, value in shop.items():
            if key not in ["name", "genre"]:
                prompt += f"""
                {key} : {value}"""
        prompts[shop_name] = prompt
    return prompts

#メイン
def main():
    st.title("ホットペッパーグルメ宣伝文生成器")
    st.sidebar.header("使い方")
    st.sidebar.info(
      '''
        飲食店の適当なキーワードを入力して、chatGPTでそのお店の宣伝文を生成してくれるアプリ
        '''
      )
    user_query = st.text_input("飲食店の検索キーワードを入力(例:「池袋　インドカレー」)", "東京　飲食店")

    prompt_dict = make_prompt_list(ask_hotpepper(user_query, 100))
    print(prompt_dict)

    shop_name = random.choice(list(prompt_dict.keys()))
    shop_prompt = prompt_dict[shop_name]

    ans_chatGPT = make_propaganda(shop_prompt)
    st.write(f"{ans_chatGPT}")
    
if __name__ == "__main__":
    main()