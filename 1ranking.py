import pandas as pd
import json

file_path = "成績表.xlsx"
xls = pd.ExcelFile(file_path)

# シート読み込み
df_batting_details = pd.read_excel(xls, sheet_name="打撃詳細", dtype=str)
df_original = pd.read_excel(xls, sheet_name=0, dtype=str)  # 元データ（1枚目）
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
df_batting_details.update(ranking_df)# ➤ top_3_batting_simple.json（上位3人）
def extract_top_n_simple(df, columns, n=3):
    top_n_data = {}
    for col in columns:
        df_valid = df[df[col].str.strip() != ""].copy()
        df_valid[col] = df_valid[col].str.extract(r"([\d\.]+)").astype(float)
        df_valid["rank"] = df_valid[col].rank(method="min", ascending=False)
        top_n = df_valid[df_valid["rank"] <= n][["打者", col, "rank"]]

        if col in ["打率", "出塁率", "OPS"]:
            top_n[col] = top_n[col].apply(lambda x: f"{x:.3f}")
        elif col == "守備率":
            top_n[col] = top_n[col].apply(lambda x: f"{int(x * 100)}%")
        else:
            top_n[col] = top_n[col].astype(int).astype(str)

        top_n = top_n.drop(columns=["rank"]).sort_values(by=col, ascending=False)
        top_n_data[col] = top_n.to_dict(orient="records")
    return top_n_data

top_3_simple = extract_top_n_simple(ranking_df.copy(), rank_columns, n=3)
with open("0ranking.json", "w", encoding="utf-8") as f:
    json.dump(top_3_simple, f, ensure_ascii=False, indent=4)

print("ranking完成")