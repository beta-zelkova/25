import pandas as pd # type: ignore
import json

# ファイルパス
file_path = "成績表.xlsx"

# Excelファイルを読み込む（すべての値を文字列として扱う）
xls = pd.ExcelFile(file_path)
df_batting = pd.read_excel(xls, sheet_name="打撃", dtype=str)
df_batting_details = pd.read_excel(xls, sheet_name="打撃詳細", dtype=str)
df_result = pd.read_excel(xls, sheet_name="打席結果", dtype=str)

df_batting = df_batting.fillna("")
df_batting_details = df_batting_details.fillna("")
df_result = df_result.fillna("")

# 順位付けが必要な指標
rank_columns = ["打率", "出塁率", "OPS", "守備率", "安打", "盗塁", "本塁打", "打点"]

# 順位付けの対象者（全体を除外）
ranking_df = df_batting_details[df_batting_details["打者"] != "全体"].copy()

# 順位付け処理
def rank_column(df, column):
    df["rank"] = df[column].astype(float).rank(method="min", ascending=False).astype(int)
    df[column] = df[column] + " (" + df["rank"].astype(str) + ")"
    df.drop(columns=["rank"], inplace=True)
    return df

for col in rank_columns:
    ranking_df = rank_column(ranking_df, col)



# 元データに反映
df_batting_details.update(ranking_df)

# DataFrameをJSONに変換（数値を文字列として維持）
batting_json = df_batting.to_dict(orient="records")
batting_details_json = df_batting_details.to_dict(orient="records")
batting_result_json = df_result.to_dict(orient="records")


# JSONファイルとして保存
batting_json_path = "batting_data.json"
batting_details_json_path = "DETAIL_DATA.json"
batting_result_json_path="at_bat_result.json"

with open(batting_json_path, "w", encoding="utf-8") as f:
    json.dump(batting_json, f, ensure_ascii=False, indent=4)

with open(batting_details_json_path, "w", encoding="utf-8") as f:
    json.dump(batting_details_json, f, ensure_ascii=False, indent=4)

with open(batting_result_json_path, "w", encoding="utf-8") as f:
    json.dump(batting_result_json, f, ensure_ascii=False, indent=4)

print(f"JSONファイルを保存しました: {batting_json_path}, {batting_details_json_path}")

# 上位N人を抽出する関数（同率順位を考慮し、降順にソート）
def extract_top_n_simple(df, columns, n=3):
    top_n_data = {}
    for col in columns:
        # 数値に変換してソート
        df[col] = df[col].str.extract(r"([\d\.]+)").astype(float)
        df["rank"] = df[col].rank(method="min", ascending=False)  # 順位を計算
        top_n = df[df["rank"] <= n][["打者", col, "rank"]]  # 指定順位以内を抽出

        # 指標ごとにフォーマットを適用
        if col in ["打率", "出塁率", "OPS"]:
            top_n[col] = top_n[col].apply(lambda x: f"{x:.3f}")  # 小数点以下第三位まで
        elif col == "守備率":
            top_n[col] = top_n[col].apply(lambda x: f"{int(x * 100)}%")  # パーセンテージ表記（小数不要）
        else:
            top_n[col] = top_n[col].astype(int).astype(str)  # 整数表記

        # rank列を削除し、降順にソート
        top_n = top_n.drop(columns=["rank"]).sort_values(by=col, ascending=False)  # 指標値で降順ソート
        top_n_data[col] = top_n.to_dict(orient="records")  # 指標ごとに辞書形式で保存
    return top_n_data

# 上位N人を抽出（簡易形式）
top_3_simple = extract_top_n_simple(ranking_df, rank_columns, n=3)

# JSONファイルとして保存
top_3_simple_json_path = "top_3_batting_simple.json"
with open(top_3_simple_json_path, "w", encoding="utf-8") as f:
    json.dump(top_3_simple, f, ensure_ascii=False, indent=4)

print(f"上位3人の簡易データを保存しました: {top_3_simple_json_path}")