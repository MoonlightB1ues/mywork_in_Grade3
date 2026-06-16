import requests
from bs4 import BeautifulSoup
import json
import time
import random
import pandas as pd
import numpy as np

import statsmodels.api as sm
from datetime import datetime, timedelta
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import re

import warnings
# 忽略 pandas 的某些切片警告
warnings.filterwarnings('ignore')
#接入ip池

# 隧道域名:端口号
tunnel = "a643.kdltpspro.com:15818"

# 用户名密码方式
username = "t17993203719190"
password = "kn35abpx"
proxies = {
    "http": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": tunnel},
    "https": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": tunnel}
}



class BaseScraper:
    """基础爬虫类：封装反爬策略与重试机制"""

    def __init__(self):
        self.session = requests.Session()
        # 挂载自动重试机制：应对 429 频次限制和 50x 服务器错误
        retry = Retry(total=5, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)

        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0'
        ]

    def get_headers(self):
        return {
            'User-Agent': random.choice(self.user_agents)
}

    def adaptive_sleep(self, min_s=0.5, max_s=1):
        """自适应随机休眠，避免呈现机器周期性特征"""
        time.sleep(random.uniform(min_s, max_s))


class Task1_GubaScraper(BaseScraper):
    """任务一：东方财富股吧数据爬取"""

    def __init__(self, stock_code, pages_to_scrape):
        super().__init__()
        self.stock_code = stock_code
        self.pages_to_scrape = pages_to_scrape
        self.base_url = f"https://guba.eastmoney.com/list,{self.stock_code}_{{}}.html"
        self.output_file = f"guba{stock_code}.txt"
        self.current_year = datetime.now().year
        self.last_seen_month = datetime.now().month

    def parse_date(self, date_str):
        """处理时间字符串，增加双向跨年校验以应对交界处乱序跳动"""
        try:
            date_str = date_str.strip()
            if len(date_str) == 11:  # 假设格式是 12-31 14:30
                current_month = int(date_str.split('-')[0])

                # 【核心逻辑升级：双向年份校准】
                month_diff = current_month - self.last_seen_month

                # 情况1：年初 -> 年底 (例如 1月跳到12月，差值是 11)
                # 触发场景：倒序爬取时正常跨年，或者在年初遇到了去年底被顶上来的旧帖
                # 设定阈值 >= 9（涵盖一季度跳四季度的情况）
                if month_diff >= 9:
                    self.current_year -= 1

                # 情况2：年底 -> 年初 (例如 12月跳回1月，差值是 -11)
                # 触发场景：跨年交界处的乱序！刚处理完去年底的帖子，下一条又是今年初的帖子
                elif month_diff <= -9:
                    self.current_year += 1

                # 注：较小的差值（例如 5月跳到 3月，或者 2月遇到去年 8月的随机老帖）
                # 均不触发年份变动，保持当前基准年份即可

                # 更新状态基准
                self.last_seen_month = current_month
                return f"{self.current_year}-{date_str}"

            return date_str

        except Exception as e:
            print(f"日期解析错误, 原数据: '{date_str}', 错误: {e}")
            return date_str

    def run(self):
        print(f"--- 开始执行任务 1：爬取长久物流股吧前 {self.pages_to_scrape} 页数据 ---")
        all_posts = []

        for page in range(1, self.pages_to_scrape + 1):
            url = self.base_url.format(page)
            try:
                resp = requests.get(url, headers=self.get_headers(),proxies=proxies,timeout=100)
                print(resp.status_code)
                resp.encoding = 'utf-8'
                soup = BeautifulSoup(resp.text, 'html.parser')

                # 【修改1：适配新的 Table 行结构】
                items = soup.select('tr.listitem')

                for item in items:
                    # 【修改2：适配新的数据字段类名】
                    read_cnt=item.find("div", attrs={"class": "read"}).text
                    # comment_cnt = item.select_one('div.reply').text.strip() if item.select_one('div.reply') else '0'
                    comment_cnt = item.find("div",attrs={"class":"reply"}).text
                    author_cnt = item.find("div",attrs={"class":"author"}).text
                    # 提取标题和链接
                    title_tag = item.select_one('div.title a')
                    # 【修改3：新版标题文字在标签内部，不在 title 属性里了】
                    # title = title_tag.text.strip() if title_tag else ''
                    title= f"'{title_tag.text.strip()}'" #这样读取出的文本更安全
                    post_time_raw = item.select_one('div.update').text.strip() if item.select_one('div.update') else ''

                    # 【修改5：修复之前的“万”字转换 Bug，支持小数运算】
                    if '万' in read_cnt:
                        read_cnt = str(int(float(read_cnt.replace('万', '')) * 10000))
                    if '万' in comment_cnt:
                        comment_cnt = str(int(float(comment_cnt.replace('万', '')) * 10000))

                    post_time = self.parse_date(post_time_raw)

                    all_posts.append(f"{post_time}\t{read_cnt}\t{comment_cnt}\t{author_cnt}\t{title}")

                print(f"第 {page} 页抓取完成，本页提取 {len(items)} 条。")
                self.adaptive_sleep()

            except Exception as e:
                print(f"第 {page} 页抓取失败: {e}")


        # 写入文件（Tab分隔，避免标题中的逗号干扰）
        with open(self.output_file, 'w', encoding='utf-8') as f:
            f.write("PostTime\tReadCount\tCommentCount\tauthor_cnt\tTitle\n")
            f.write('\n'.join(all_posts))
        print(f"任务 1 完成，数据已保存至 {self.output_file}\n")





class Task2_SinaDataFetcher(BaseScraper):
    """任务二：新浪财经历史行情数据获取"""

    def __init__(self, symbol="sh603569", datalen=10000):
        super().__init__()
        self.url = f"http://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData?symbol={symbol}&scale=240&ma=no&datalen={datalen}"
        self.output_file = "data_sina_cjwl.txt"

    def run(self):
        print(f"--- 开始执行任务 2：拉取新浪财经 K线数据 ---")
        try:
            resp = self.session.get(self.url, headers=self.get_headers(), timeout=10)
            # 新浪API返回的JSON Key没有双引号，需使用正则补全或转化为标准JSON
            json_str = re.sub(r'([{,])([a-zA-Z_]+):', r'\1"\2":', resp.text)
            data = json.loads(json_str)

            with open(self.output_file, 'w', encoding='utf-8') as f:
                f.write("Date,Open,High,Low,Close,Volume\n")
                for day_data in data:
                    line = f"{day_data['day']},{day_data['open']},{day_data['high']},{day_data['low']},{day_data['close']},{day_data['volume']}"
                    f.write(line + "\n")
            print(f"任务 2 完成，共获取 {len(data)} 个交易日数据，已保存至 {self.output_file}\n")

        except Exception as e:
            print(f"任务 2 执行失败: {e}")


class Task3_FactorAnalysis:
    """任务三：指标构建与回归检验"""

    def __init__(self):
        self.guba_file = "guba603569.txt"
        self.sina_file = "data_sina_cjwl.txt"

    def run(self):
        print(f"--- 开始执行任务 3：构建信息量指标及超额收益率检验 ---")
        # 1. 处理股吧数据
        try:
            df_guba = pd.read_csv(self.guba_file, sep='\t',on_bad_lines='skip')
        except FileNotFoundError:
            print("未找到股吧数据，请先成功运行任务 1")
            return

        # 提取日期部分 (YYYY-MM-DD)
        df_guba['Date'] = df_guba['PostTime'].astype(str).str[:10]  #剔除了时分的信息
        # 转换数值
        df_guba['ReadCount'] = pd.to_numeric(df_guba['ReadCount'], errors='coerce').fillna(0)  # coercen把异常数据处理为nan,fillna把nan处理为0
        df_guba['CommentCount'] = pd.to_numeric(df_guba['CommentCount'], errors='coerce').fillna(0)

        # 【指标设计】：信息关注度因子 (InfoFactor)
        # 逻辑：当日发帖总数 + 权重*(ln(阅读量+1) + ln(评论数+1)) 的日度求和
        # 按日聚合成因子日序列
        factor_daily = df_guba.groupby('Date').agg(
            cul_read = ('ReadCount','sum'),
            cul_comment = ('CommentCount','sum'),
            cul_post = ("Title",'size')
        ).reset_index()


        factor_daily['Date'] = pd.to_datetime(factor_daily['Date'],format='%Y-%m-%d')
        row_nums = np.arange(1, len(factor_daily) + 1)
        factor_daily["InfoFactor"]=(np.log(factor_daily['cul_read']+1)+factor_daily['cul_comment']*factor_daily['cul_post'])/(np.log(row_nums+1))
        path = '/QuantativeFinancial/home6/get/result.csv'
        factor_daily.to_csv(path,index=False, encoding='utf-8-sig')
        # 2. 处理行情数据
        try:
            df_price = pd.read_csv(self.sina_file)
        except FileNotFoundError:
            print("未找到行情数据，请先成功运行任务 2")
            return

        df_price['Date'] = pd.to_datetime(df_price['Date'])
        df_price = df_price.sort_values('Date')

        # 计算日度收益率: R_t = (Close_t - Close_{t-1}) / Close_{t-1}
        df_price['Return'] = df_price['Close'].pct_change()

        # 计算超额收益率（此处简化：减去无风险利率近似值 0.03/252，若有沪深300数据可减去基准收益率）
        rf_daily = 0.03 / 252
        df_price['ExcessReturn'] = df_price['Return'] - rf_daily

        # 3. 数据合并对齐
        # 我们用 t-1 日的因子（盘后发酵情绪），预测 t 日的超额收益率
        df_merged = pd.merge(df_price, factor_daily, on='Date', how='left')
        df_merged['InfoFactor'] = df_merged['InfoFactor'].fillna(0)  # 没发帖的日子因子为0

        # 特征滞后一期：Shift因子
        df_merged['Lagged_InfoFactor'] = df_merged['InfoFactor'].shift(1)

        # 剔除空值
        df_reg = df_merged.dropna(subset=['ExcessReturn', 'Lagged_InfoFactor'])

        if len(df_reg) < 30:
            print("有效样本量过少，无法进行稳健的回归分析。请增加爬取的股吧页数。")
            return

        # 4. OLS 回归检验
        # 模型：ExcessReturn_t = α + β * InfoFactor_{t-1} + ε
        X = df_reg['Lagged_InfoFactor']
        X = sm.add_constant(X)  # 添加截距项 α
        Y = df_reg['ExcessReturn']

        model = sm.OLS(Y, X).fit()

        print("\n=== 信息关注度因子 OLS 回归检验结果 ===")
        print(model.summary())
        print("\n结论分析：")
        p_value = model.pvalues['Lagged_InfoFactor']
        coef = model.params['Lagged_InfoFactor']
        if p_value < 0.05:
            print(f"Lagged_InfoFactor 的 p 值为 {p_value:.4f} < 0.05，在统计学上显著。")
            print(f"系数为 {coef:.6f}，说明前一日股吧信息量每增加 1 个单位，次日超额收益预期变化 {coef * 100:.4f}%。")
        else:
            print(f"Lagged_InfoFactor 的 p 值为 {p_value:.4f} >= 0.05，在统计学上不显著。")
            print(
                "这表明单纯基于发帖量和阅读评论构建的基础因子，在当前样本区间内无法有效预测长久物流的次日超额收益率。建议引入NLP进行情感分析（看多/看空）来深化因子。")


if __name__ == "__main__":
    # 执行任务一：组队分工时，可调整 pages_to_scrape 参数（例如爬取 20 页）
    # scraper = Task1_GubaScraper(stock_code="603569", pages_to_scrape=600)
    # scraper.run()

    # 执行任务二：获取行情
    fetcher = Task2_SinaDataFetcher()
    fetcher.run()

    # 执行任务三：因子验证回归
    analyzer = Task3_FactorAnalysis()
    analyzer.run()