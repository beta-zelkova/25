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