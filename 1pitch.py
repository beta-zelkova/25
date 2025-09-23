import pandas as pd

def clean_column_names(columns):
    return [str(col).strip().replace(" ", "_").replace(".", "").replace(":", "")
            .replace("●", "loss_mark").replace("Unnamed", "col")
            for col in columns]

def row_to_sql_insert(table_name, row):
    columns = ", ".join(row.index)
    values = []
    for value in row:
        if pd.isna(value):
            values.append("NULL")
        elif isinstance(value, str):
            safe_value = value.replace("'", "''").replace("\n", "\\n").replace("\r", "")
            values.append(f"'{safe_value}'")
        else:
            values.append(str(value))
    return f"INSERT INTO {table_name} ({columns}) VALUES ({', '.join(values)});"

# Excelファイルの読み込み
file_path = "成績表.xlsx"
df_togen = pd.read_excel(file_path, sheet_name="投元")
df_toshu = pd.read_excel(file_path, sheet_name="投手")

# 列名クリーンアップ
df_togen.columns = clean_column_names(df_togen.columns)
df_toshu.columns = clean_column_names(df_toshu.columns)

# 投元 → pitch_logs.sql
with open("pitch_logs.sql", "w", encoding="utf-8") as f_logs:
    for _, row in df_togen.iterrows():
        f_logs.write(row_to_sql_insert("pitch_logs", row) + "\n")

# 投手 → pitch_stats.sql
with open("pitch_stats.sql", "w", encoding="utf-8") as f_stats:
    for _, row in df_toshu.iterrows():
        f_stats.write(row_to_sql_insert("pitch_stats", row) + "\n")

print("✅ SQLファイルを個別に生成しました:")
print("   - pitch_logs.sql（投元）")
print("   - pitch_stats.sql（投手）")
print("✅ 完了")