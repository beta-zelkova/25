import pandas as pd
import json

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
with open('0result.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print("✅ JSONファイルを出力しました：output.json")
