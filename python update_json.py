import pandas as pd

# ファイル名の設定
EXCEL_FILE = "成績表.xlsx"
JSON_FILE = "batting_data.json"
JSON_FILE_DETAIL = "DETAIL_DATA.json"
CSV_FILE = "batting_data.csv"

def update_json():
    try:
        df = pd.read_excel(EXCEL_FILE, sheet_name="打撃")
        df2 = pd.read_excel(EXCEL_FILE, sheet_name="打撃詳細") 
        df.to_json(JSON_FILE, orient="records", force_ascii=False, indent=4)
        df2.to_json(JSON_FILE_DETAIL, orient="records",force_ascii=False,indent=4)
        df.to_csv(CSV_FILE, index=False, encoding="utf-8-sig")
        print(f"JSON と CSV を更新しました。")
    except Exception as e:
        print(f"エラー: {e}")

if __name__ == "__main__":
    update_json()


import pandas as pd

# 丸数字を用意
rank_symbols = ["①", "②", "③", "④", "⑤", "⑥", "⑦", "⑧", "⑨", "⑩"]

# JSON ファイルの読み込み
df = pd.read_json("batting_data.json")

# 順位を計算する指標を指定
ranking_metrics = ["打率", "出塁率", "OPS"]

for metric in ranking_metrics:
    df[metric] = pd.to_numeric(df[metric], errors='coerce')  # 数値変換
    df = df.sort_values(by=metric, ascending=False).reset_index(drop=True)
    df[f"{metric}順位"] = [rank_symbols[i] if i < len(rank_symbols) else str(i+1) for i in range(len(df))]

# JSONに出力
df.to_json("batting_data.json", orient="records", force_ascii=False, indent=4)
