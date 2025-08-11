import os
from dotenv import load_dotenv
from openai import OpenAI
from newspaper import Article
import json

# 加载环境变量
load_dotenv()

# 从环境变量获取配置
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_API_BASE = os.getenv('OPENAI_API_BASE')

try:
    with open('articles.json', 'r', encoding='utf-8') as f:
            articles = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
        articles = []

beatify_prompt = """
你是一名专业的新闻编辑，负责将文章内容进行美化和润色。
用户将给你一篇文章，你需要对其进行润色和美化，但请注意，不要修改原文，删除正文除外的内容，如“***出品”，“扫码下方二维码”、“推荐阅读”，改正newspaper提取之后存在的错乱的符号和格式问题
此外，你需要返回一个你认为文章中需要画出的关键语句，多画几个句子，按照重要程度分别画出红色和绿色笔记，分别使用<red>和<green>标签
注意输出结果严格以传入的 json 格式返回，文章标题千万不能出现空格等特殊字符，文章内容不要出现双换行符，只留一个，示例如下
{
  "title": "中国人民银行宣布将实施八项政策举措-新华网",
  "content": "新华社上海6月18日电（记者吴雨、桑彤）<red>18日，中国人民银行行长潘功胜在2025陆家嘴论坛上宣布，将在上海实施八项政策举措。</red>一是设立银行间市场交易报告库。高频汇集并系统分析银行间债券、货币、衍生品、黄金、票据等各金融子市场交易数据，服务金融机构、宏观调控和金融市场监管。<green>二是设立数字人民币国际运营中心。推进数字人民币的国际化运营与金融市场业务发展，服务数字金融创新。</green>三是设立个人征信机构。为金融机构提供多元化、差异化的个人征信产品，进一步健全社会征信体系。四是在上海临港新片区开展离岸贸易金融服务综合改革试点。创新业务规则，支持上海发展离岸贸易。五是发展自贸离岸债。遵循“两头在外”的原则和国际通行的规则标准，拓宽“走出去”企业及“一带一路”共建国家和地区优质企业的融资渠道。六是优化升级自由贸易账户功能。实现优质企业与境外资金高效融通，提升跨境贸易投资自由化便利化水平。七是在上海“先行先试”结构性货币政策工具创新。包括开展航贸区块链信用证再融资业务、“跨境贸易再融资”业务、碳减排支持工具扩容等试点，积极推动上海首批运用科技创新债券风险分担工具，支持私募股权机构发行科创债券。八是会同证监会研究推进人民币外汇期货交易。推动完善外汇市场产品序列，便利金融机构和外贸企业更好管理汇率风险。"
}
"""
ask_prompt = """
你是一名文章内容解读专家，负责解答用户的问题
注意，严格避免出现任何 markdown md 语法如 `-`、`**` 和html语法
文章内容如下：
"""

client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_API_BASE
)

def fetch_article(url: str):
    article = Article(url, language='zh')
    article.download()
    article.parse()
    return article

def beatify_article(article: Article):
    article.nlp()
    response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {
            "role": "system",
            "content": beatify_prompt,
        },
        {
            "role": "user",
            "content": f'{{"title": "{article.title}", "content": "{article.summary}"}}'
        },
    ],
    stream=False
    )
    return response.choices[0].message.content
def ask_ai(question: str , index: int):
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {
                "role": "system",
                "content": ask_prompt + articles[index]["content"]
            },
            {
                "role": "user",
                "content": question
            }
        ],
        stream=False
    )
    return response.choices[0].message.content
if __name__ == "__main__":
    url = 'http://politics.people.com.cn/n1/2025/0618/c1024-40502834.html'
    article = fetch_article(url)
    beautified_article = beatify_article(article)
    if beautified_article:
        articles.append(json.loads(beautified_article))
        with open('articles.json', 'w', encoding='utf-8') as f:
            json.dump(articles, f, ensure_ascii=False, indent=4)
        print(ask_ai("这篇文章讲了什么",0))