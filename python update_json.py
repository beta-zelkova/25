import pandas as pd

# ファイル名の設定
EXCEL_FILE = "成績表.xlsx"
JSON_FILE_DETAIL = "DETAIL_DATA.json"
JSON_FILE = "batting_data.json"

# 丸数字リスト
rank_symbols = ["①", "②", "③", "④", "⑤", "⑥", "⑦", "⑧", "⑨", "⑩"]

def attach_ranking(df, column):
    """ 指定した指標に丸数字で順位を付加し、小数点以下3桁を維持 """
    if column not in df.columns:
        print(f"警告: {column} がデータに存在しません")
        return df  # 指標がなければスキップ

    df[column] = pd.to_numeric(df[column], errors='coerce')  # 数値変換（エラー時 NaN）
    df = df.sort_values(by=column, ascending=False, na_position='last').reset_index(drop=True)  # 降順ソート
    df[f"{column}順位"] = [rank_symbols[i] if i < len(rank_symbols) else str(i+1) for i in range(len(df))]

    # 小数点以下3桁を維持し、丸数字を追加（NaN の場合はそのまま）
    df[column] = df.apply(lambda row: f"{row[column]:.3f}{row[f'{column}順位']}" if pd.notna(row[column]) else "-", axis=1)

    df.drop(columns=[f"{column}順位"], inplace=True)  # 不要な順位カラム削除
    return df

def update_json():
    try:
        # Excel のデータを読み込む
        df2 = pd.read_excel(EXCEL_FILE, sheet_name="打撃詳細")
        df3 = pd.read_excel(EXCEL_FILE, sheet_name="打撃")


        # 順位を付加する指標
        ranking_metrics = ["打率", "出塁率", "OPS"]

        # 各指標の処理
        for metric in ranking_metrics:
            df2 = attach_ranking(df2, metric)

        # JSON, CSV 出力（force_ascii=False で日本語を維持）
        df2.to_json(JSON_FILE_DETAIL, orient="records", force_ascii=False, indent=4)
        df3.to_json(JSON_FILE, orient="records", force_ascii=False, indent=4)

        print("DETAIL_DATA.json を更新しました。")

    except Exception as e:
        print(f"エラー発生: {e}")

if __name__ == "__main__":
    update_json()

