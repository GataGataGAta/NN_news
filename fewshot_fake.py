from openai import OpenAI
import os
import random as rand

from datetime import datetime

def get_timestamp_str():
    now = datetime.now()
    return now.strftime('%y_%m_%d_%H_%M_%S')

# 使用例

N=15

# APIキーを環境変数から取得
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

#フェイクニュースのジャンル
K = ["経済", "政治", "科学", "スポーツ", "IT"]
K_count = [5 for i in range(len(K))]

for i in range(N):

    #ジャンルをランダムで指定
    index = rand.randint(0,len(K))%len(K)
    k = K[index]
    print(k)

    # few-shotプロンプトの例（ショット）
    messages = [
        {"role": "system", "content": "あなたはフェイクニュースを創作するAIです。ジャンルごとにありそうでなさそうなニュースを考えます。実在する人物、団体名は使用せず少し変えます。"},
        
        # ショット1（スポーツ）
        {"role": "user", "content": "スポーツのフェイクニュースを考えて"},
        {"role": "assistant", "content": "【速報】小谷修平選手、離婚を発表 愛犬の命名めぐる“デコポン騒動”が原因か\n米メジャーリーグ・ドヤースで活躍中の小谷修平選手が、現地時間24日、妻との離婚を発表した。関係者によると、離婚理由として「愛犬の名前をめぐる意見の対立」があったという。\n小谷選手は、最近家族に迎え入れた愛犬に「デコポン」と名付けたいという強い希望を持っていたが、妻はこれに納得せず、夫婦間でたびたび言い争いになっていたとされる。こうした小さな対立が積み重なり、最終的に離婚という形に至った模様だ。\nチーム関係者は「私生活での出来事ではあるが、チーム活動には支障なく取り組んでいる」とコメント。小谷選手本人もSNSで「今後も変わらず応援していただけたら嬉しいです」と心境を語っている。"},
        
        # ショット2（経済）
        {"role": "user", "content": "経済のフェイクニュースを考えて"},
        {"role": "assistant", "content": "新しい通貨『グローバルコイン』が来月から世界中で使用開始！？\n世界銀行と主要な経済大国が共同で開発した新しいデジタル通貨「グローバルコイン」が来月から公式に導入されることが発表された。この通貨は、既存のすべての国の通貨に取って代わるもので、国際貿易を大幅に簡素化することが期待されている。各国政府はすでにこの計画を承認しており、国民は今後、現金や既存のデジタル通貨をすべてグローバルコインに変換することが義務付けられるという。\nこのニュースは多くの経済専門家から批判を受けており、一部の専門家は、各国の通貨主権が失われる可能性を懸念している。しかし、支持者たちは、グローバルな経済成長を促進し、為替リスクを排除する画期的なステップであると主張している。"},
        
        # テストプロンプト（科学）
        {"role": "user", "content": k+"のフェイクニュースを考えて"}
    ]

        # 応答生成
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        temperature=0.7
    )

    # 応答の取り出し
    timestamp = get_timestamp_str()
    news = completion.choices[0].message.content
    
    # テキストファイルに書き込み
    output_path ="news\\"+"fake_news_"+k+timestamp+".txt"
    K_count[index]+=1

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(news)

    # コンソールにも出力
    #print(f"生成されたフェイクニュースを「{output_path}」に保存しました。\n\n内容:\n{news}")
