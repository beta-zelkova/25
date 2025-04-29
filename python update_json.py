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
df_batting_details.update(ranking_df)

# ➤ DETAIL_DATA.json（順位付き）
detail_json = df_batting_details.to_dict(orient="records")
with open("DETAIL_DATA.json", "w", encoding="utf-8") as f:
    json.dump(detail_json, f, ensure_ascii=False, indent=4)

# ➤ batting_data.json（順位なし：数値のみ）
batting_columns = [
    "打者", "試合", "打席", "打数", "安打", "二塁打", "三塁打", "本塁打",
    "塁打", "打点", "得点", "三振", "四球", "死球", "犠打", "犠飛",
    "盗塁", "盗塁刺", "併殺", "打率", "出塁率", "長打率", "OPS"
]

df_batting_no_rank = df_batting_details.copy()
for col in rank_columns:
    if col in df_batting_no_rank.columns:
        df_batting_no_rank[col] = df_batting_no_rank[col].str.extract(r"([\d\.]+)").fillna("").astype(str)

available_columns = [col for col in batting_columns if col in df_batting_no_rank.columns]
df_batting_from_details = df_batting_no_rank[available_columns].copy()

batting_json = df_batting_from_details.to_dict(orient="records")
with open("batting_data.json", "w", encoding="utf-8") as f:
    json.dump(batting_json, f, ensure_ascii=False, indent=4)

# ➤ at_bat_result.json（元データのA～D列＋AE～AJ列 → インデックスで 0–3 + 30–35）
at_bat_indices = list(range(0, 4)) + list(range(30, 36))
max_col = len(df_original.columns)
valid_indices = [i for i in at_bat_indices if i < max_col]
selected_columns = df_original.columns[valid_indices]

df_result = df_original[selected_columns].copy().fillna("")

batting_result_json = df_result.to_dict(orient="records")
with open("at_bat_result.json", "w", encoding="utf-8") as f:
    json.dump(batting_result_json, f, ensure_ascii=False, indent=4)

# ➤ top_3_batting_simple.json（上位3人）
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
with open("top_3_batting_simple.json", "w", encoding="utf-8") as f:
    json.dump(top_3_simple, f, ensure_ascii=False, indent=4)

print("✅ すべてのJSONファイルを正常に保存しました（打席結果は元データから抽出）")


# Excelファイルを読み込む（"元データ"シート）
df = pd.read_excel('成績表.xlsx', sheet_name='元データ', engine='openpyxl')

# 出力リスト
output = []

# 各行を処理
for _, row in df.iterrows():
    opponent = row.iloc[0]             # A列：対戦相手
    position1 = row.iloc[2]            # C列：守備位置1
    position2 = row.iloc[3]            # D列：守備位置2
    player = row.iloc[29]              # AD列：選手名（0始まりで29列目）
    atbats = row.iloc[30:36]           # AE〜AJ列：打席結果（30〜35列目）

    if pd.isna(player):
        continue  # 選手名がない行はスキップ

    data = {
        "対戦相手": opponent if not pd.isna(opponent) else "",
        "守備位置": [p for p in [position1, position2] if not pd.isna(p)],
        "選手名": player,
        "打席結果": [res for res in atbats if not pd.isna(res)]
    }

    output.append(data)

# JSONに書き出し
with open('at_bat_result.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print("✅ JSONファイルを出力しました：output.json")
