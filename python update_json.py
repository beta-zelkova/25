import pandas as pd

# ファイル名の設定
EXCEL_FILE = "成績表.xlsx"
JSON_FILE_DETAIL = "DETAIL_DATA.json"

# 丸数字リスト
rank_symbols = ["①", "②", "③", "④", "⑤", "⑥", "⑦", "⑧", "⑨", "⑩"]

def attach_ranking(df, column):
    """ 指定された指標に丸数字で順位を付加する（値の右側に追加） """
    if column not in df.columns:
        print(f"警告: {column} がデータに存在しません")
        return df  # 指標がなければスキップ

    df[column] = pd.to_numeric(df[column], errors='coerce')  # 数値変換（エラー時 NaN）
    df = df.sort_values(by=column, ascending=False, na_position='last').reset_index(drop=True)  # 降順ソート
    df[f"{column}順位"] = [rank_symbols[i] if i < len(rank_symbols) else str(i+1) for i in range(len(df))]

    # 成績の数値に丸数字を追加（NaN の場合はそのまま）
    df[column] = df.apply(lambda row: f"{row[column]}{row[f'{column}順位']}" if pd.notna(row[column]) else "-", axis=1)

    df.drop(columns=[f"{column}順位"], inplace=True)  # 不要な順位カラム削除
    return df

def update_json():
    try:
        # Excel のデータを読み込む
        df2 = pd.read_excel(EXCEL_FILE, sheet_name="打撃詳細")

        # 確認用: 読み込んだデータのカラム一覧を表示
        print("読み込んだカラム:", df2.columns.tolist())

        # 順位を付加する指標
        ranking_metrics = ["打率", "出塁率", "OPS"]

        # 各指標の処理
        for metric in ranking_metrics:
            df2 = attach_ranking(df2, metric)

        # JSON, CSV 出力
        df2.to_json(JSON_FILE_DETAIL, orient="records", force_ascii=False, indent=4)

        print("DETAIL_DATA.json を更新しました。")

    except Exception as e:
        print(f"エラー発生: {e}")

if __name__ == "__main__":
    update_json()
