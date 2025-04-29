import pandas as pd
import json

# Excelファイルのパス
file_path = "成績表.xlsx"
xls = pd.ExcelFile(file_path)

# シート読み込み
df_batting_details = pd.read_excel(xls, sheet_name="打撃詳細", dtype=str)
df_original = pd.read_excel(xls, sheet_name=5, dtype=str)  # 元データ（1枚目）
df_batting_details = df_batting_details.fillna("")
df_original = df_original.fillna("")

# 順位をつける指標
rank_columns = ["打率", "出塁率", "OPS", "守備率", "安打", "盗塁", "本塁打", "打点"]
ranking_df = df_batting_details[df_batting_details["打者"] != "全体"].copy()

# 順位付け関数
def rank_column(df, column):
    df_valid = df[df[column].str.strip() != ""].copy()
    df_valid["rank"] = df_valid[column].astype(float).rank(method="min", ascending=False).astype(int)
    df_valid[column] = df_valid[column] + " (" + df_valid["rank"].astype(str) + ")"
    df.update(df_valid)
    return df

# 各項目に順位付け
for col in rank_columns:
    ranking_df = rank_column(ranking_df, col)

# 順位付きデータを元のdfに反映
df_batting_details.update(ranking_df)

# ➤ DETAIL_DATA.json（順位付き）
detail_json = df_batting_details.to_dict(orient="records")
with open("0DETAIL_DATA.json", "w", encoding="utf-8") as f:
    json.dump(detail_json, f, ensure_ascii=False, indent=4)

# ➤ batting_data.json（順位なし：数値のみ）
batting_columns = [
    "打者", "試合", "打席", "打数", "安打",  "本塁打",
    "打点", "得点", "三振", "四球", "打率", "出塁率", "OPS"
]

df_batting_no_rank = df_batting_details.copy()
for col in rank_columns:
    if col in df_batting_no_rank.columns:
        df_batting_no_rank[col] = df_batting_no_rank[col].str.extract(r"([\d\.]+)").fillna("").astype(str)

available_columns = [col for col in batting_columns if col in df_batting_no_rank.columns]
df_batting_from_details = df_batting_no_rank[available_columns].copy()

batting_json = df_batting_from_details.to_dict(orient="records")
with open("0batting_data.json", "w", encoding="utf-8") as f:
    json.dump(batting_json, f, ensure_ascii=False, indent=4)

# ➤ at_bat_result.json（元データのA～D列＋AE～AJ列 → インデックスで 0–3 + 30–35）
at_bat_indices = list(range(0, 4)) + list(range(30, 36))
max_col = len(df_original.columns)
valid_indices = [i for i in at_bat_indices if i < max_col]
selected_columns = df_original.columns[valid_indices]

df_result = df_original[selected_columns].copy().fillna("")

print("✅ JSON（各打席がキーとして分離された形式）を保存しました。")
