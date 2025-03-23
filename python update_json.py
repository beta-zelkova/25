import pandas as pd
import json

# ファイルパス
file_path = "成績表.xlsx"

# Excelファイルを読み込む
xls = pd.ExcelFile(file_path)
df_batting = pd.read_excel(xls, sheet_name="打撃", dtype=str)
df_batting_details = pd.read_excel(xls, sheet_name="打撃詳細", dtype=str)

# 順位付けが必要な指標
rank_columns = ["打率", "出塁率", "OPS", "守備率", "安打", "盗塁", "本塁打", "打点"]

# 順位付けの対象者（全体を除外）
ranking_df = df_batting_details[df_batting_details["打者"] != "全体"].copy()

# 順位付け処理
def rank_column(df, column):
    df[column] = df[column].astype(float)
    df["rank"] = df[column].rank(method="min", ascending=False).astype(int)
    df[column] = df[column].astype(str) + " (" + df["rank"].astype(str) + ")"
    df.drop(columns=["rank"], inplace=True)
    return df

for col in rank_columns:
    ranking_df = rank_column(ranking_df, col)

# 元データに反映
df_batting_details.update(ranking_df)

# DataFrameをJSONに変換
batting_json = df_batting.to_dict(orient="records")
batting_details_json = df_batting_details.to_dict(orient="records")

# JSONファイルとして保存
batting_json_path = "batting_data.json"
batting_details_json_path = "DETAIL_DATA.json"

with open(batting_json_path, "w", encoding="utf-8") as f:
    json.dump(batting_json, f, ensure_ascii=False, indent=4)

with open(batting_details_json_path, "w", encoding="utf-8") as f:
    json.dump(batting_details_json, f, ensure_ascii=False, indent=4)

print(f"JSONファイルを保存しました: {batting_json_path}, {batting_details_json_path}")
