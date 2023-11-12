# Note: you need to be using OpenAI Python v0.27.0 for the code below to work
import openai
from collections import defaultdict
import json

openai.api_key = ""

MODEL_NAME = "gpt-4-0613"
# MODEL_NAME = "gpt-3.5-turbo"

TEMPLATE_NAME = "以下の文章は、ユーザーのアンケートをまとめたものです。\
    アンケートの内容をもとに、２つの質問に回答してほしいです。\
    先に、２つの質問を提示してその後のアンケートの結果を共有します。"

ANSWER_1 = "「１つ目の質問の答え：〇〇鍋」"
QUESTION_1 = "１つ目、以下の鍋の種類と具材から、どの鍋をお勧めしますか？" + ANSWER_1 + "という形で答えてください。１つだけ選んでください \
    鍋に入っている食材は以下の通りです。"

ANSWER_2 = '「２つ目の質問の答え：{"ビタミンB": ["豚肉", "卵", "キムチ"], "鉄分": ["青菜", "えのき"], ...}」'
QUESTION_2 = "２つ目、アンケート結果をもとに取り入れた方がよい具材を答えてください。" + ANSWER_2 + "という形で答えてください。\
    栄養素ごとの食材は以下の通りです。"

ANSWER_STYLE = "質問への答えは、" +  ANSWER_1 + ANSWER_2 + "という形で答えてください。"

QUESTIONARE_RESULT_SENTENCE = "次にユーザーのアンケート結果は、以下の通りです。"

# 質問内容と回答を辞書として定義
QUESTIONS_AND_ANSWERS = {
    "キムチ鍋": {"ビタミンB": ["豚肉", "卵", "キムチ"], "鉄分": ["青菜", "えのき"], "炭水化物": ["ラーメン"]},
    "きりたんぽ鍋": {"タンパク質": ["鶏肉"], "食物繊維": ["ごぼう"], "ビタミンD": ["まいたけ"], "炭水化物": ["きりたんぽ"]},
    "味噌鍋": {"マグネシウム": ["味噌"], "タンパク質": ["鮭", "ホタテ"], "食物繊維": ["長ネギ", "白菜"], "炭水化物": ["うどん"]},
    "豆乳鍋": {"タンパク質": ["豚肉", "豆腐"], "善玉菌": ["豆乳"], "食物繊維": ["キャベツ"], "炭水化物": ["うどん"]},
}

NABE_LIST = list(QUESTIONS_AND_ANSWERS.keys())

def find_matching_nabe(input_string):
    for nabe in NABE_LIST:
        if nabe in input_string:
            return nabe
    return ""

def get_all_values(dictionary):
    return [value for values in dictionary.values() for value in values]

def get_categories_food():

    # 鍋ごとの栄養素リストを作成
    nutrients_by_pot = {}

    # 栄養素ごとのリストを作成
    nutrients_by_food = defaultdict(list)

    for pot, nutrients in QUESTIONS_AND_ANSWERS.items():
        nutrient_list = []
        for nutrient, foods in nutrients.items():
            nutrient_list.extend(foods)
            nutrients_by_food[nutrient].extend(foods)
        nutrients_by_pot[pot] = list(set(nutrient_list))

    pot_of_nutrients = ""
    # 結果を出力
    for pot, nutrients in nutrients_by_pot.items():
        pot_of_nutrients += f"{pot}={nutrients}" + "\n"

    nutrient_of_foods = ""
    # 栄養素ごとに食材をまとめて出力
    for nutrient, foods in nutrients_by_food.items():
        nutrient_of_foods += f"{nutrient}={list(set(foods))}" + "\n"

    return pot_of_nutrients, nutrient_of_foods

def question_about_nabe(answer_of_question):

    print(answer_of_question)
    pot_of_nutrients, nutrient_of_foods = get_categories_food()
    ques_sub1_sentence = QUESTION_1 + "\n" + pot_of_nutrients
    ques_sub2_sentence = QUESTION_2 + "\n" + nutrient_of_foods
    ques_sentence = ques_sub1_sentence + "\n" + ques_sub2_sentence
    user_ques_result_sentence = QUESTIONARE_RESULT_SENTENCE + "\n" + answer_of_question

    message = TEMPLATE_NAME + "\n" + ques_sentence + "\n" + user_ques_result_sentence + "\n" + ANSWER_STYLE
    print("###送ったメッセージ内容は下記の通りです###")
    print(message)
    print("####")
    response = openai.ChatCompletion.create(
    model = MODEL_NAME ,
    messages=[
            {"role": "user", "content": message},
        ]
    )

    print("###アンサー###")
    output = response.choices[0]["message"]["content"]
    print(output)

    # １つ目の答えを取得
    answer1_start = output.find("１つ目の質問の答え：") + len("１つ目の質問の答え：")
    answer1_end = output[answer1_start:].find("鍋")
    # 空文字の可能性あり
    answer1_split = output[answer1_start:][:answer1_end + 1].strip() if answer1_start != -1 and answer1_end + 1 != -1 else ""
    if answer1_split != "" :
        answer1 = find_matching_nabe(answer1_split)
    else :
        answer1 = answer1_split
    print("１つ目の答え:", answer1)

    # ２つ目の答えを取得
    answer2_start = output.find("２つ目の質問の答え：") + len("２つ目の質問の答え：")
    answer2_end = output[answer2_start:].find("}")
    answer2_str = output[answer2_start:][:answer2_end + 1].strip()
    try:
        answer2 = json.loads(answer2_str)
        answer2 = list(set(get_all_values(answer2)))
    except json.JSONDecodeError:
    # 辞書型が空の可能性あり
        answer2 = {}
    print("２つ目の答え:", answer2)
    
    return answer1, answer2