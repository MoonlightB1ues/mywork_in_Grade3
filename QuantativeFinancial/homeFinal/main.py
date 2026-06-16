import pandas as pd
from openai import OpenAI
import time
import json
from google import genai
from google.genai import types


# 1. 初始化大模型客户端（以兼容 OpenAI 格式的接口为例）
# client = OpenAI(
#     api_key="你的_API_KEY",
#     base_url="https://api.your-model-provider.com/v1"  # 替换为提供商的Base URL
# )

client = genai.Client()

# 2. 读取你的爬虫数据
# 假设你的csv文件有一列叫 'comment'
df = pd.read_csv('guba_comments.csv')

# 用于存储结果的列表
results = []

# 3. 循环遍历每一条评论
for index, row in df.iterrows():
    comment = row['comment']

    # 构建 Prompt
    prompt = f"""你是一个资深的金融情感分析专家。请分析以下股民评论，给出 -1(极度悲观) 到 1(极度乐观) 的情绪得分。
    严格以JSON格式输出：{{"score": 打分, "reason": "简短理由"}}
    评论内容：{comment}"""

    try:
        # 4. 发送请求给大模型
        response = client.chat.completions.create(
            model="你的模型名称",  # 例如 "gemini-1.5-pro", "deepseek-chat" 等
            messages=[
                {"role": "system", "content": "你是一个金融情感分析助手。"},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},  # 强制返回 JSON (部分模型支持)
            temperature=0.1  # 温度设低一点，保证打分标准的一致性
        )

        # 5. 解析 AI 的回答
        ai_reply = response.choices[0].message.content
        result_dict = json.loads(ai_reply)
        results.append(result_dict)

        # 打印进度
        print(f"已处理第 {index + 1} 条: 得分 {result_dict.get('score')}")

    except Exception as e:
        print(f"处理第 {index + 1} 条时出错: {e}")
        results.append({"score": None, "reason": "Error"})

    # 6. 控制请求频率（非常重要！）
    # 大多数 API 都有并发限制，加个小延迟防止被封禁
    time.sleep(0.5)

# 7. 将结果合并回原始数据并保存
results_df = pd.DataFrame(results)
df['ai_score'] = results_df['score']
df['ai_reason'] = results_df['reason']

df.to_csv('guba_comments_scored.csv', index=False, encoding='utf-8-sig')
print("全部处理完成，已保存至 csv！")