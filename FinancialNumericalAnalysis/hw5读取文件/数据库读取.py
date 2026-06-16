from sqlalchemy import create_engine, inspect,text
import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from envs.my_pythorch.Lib.unittest.mock import inplace
plt.rcParams.update({"font.family": "STIXGeneral",
                     "font.size": 20,
                     "mathtext.fontset": "cm"})

# 创建数据库连接
engine = create_engine(
    "mysql+pymysql://student:Python_123456@59.78.102.118:23208/research?charset=utf8mb4"
)

# 创建 inspector 对象
inspector = inspect(engine)
# 获取所有表名
tables = inspector.get_table_names()
print("数据库中的表有：")
for t in tables:
    print(" -", t)
columns = inspector.get_columns('balance_sheet')
print("\n表 stock_prices 的字段信息：")
for col in columns:
    print(col['name'])

sql = """
SELECT Stkcd,Date, Close,Name
FROM stock_trading_data
WHERE Stkcd="000006"

"""

df = pd.read_sql(sql, engine)
print(df)