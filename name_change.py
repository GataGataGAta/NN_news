import os

def rename_subfolders_to_numbers_in_order(target_path):
    # サブフォルダだけを取得（ファイルは無視）
    subfolders = [name for name in os.listdir(target_path)
                  if os.path.isdir(os.path.join(target_path, name))]

    # リネーム用の一時プレフィックス（衝突防止用）
    temp_mapping = {}
    for i, old_name in enumerate(subfolders, start=1):
        old_path = os.path.join(target_path, old_name)
        temp_name = f"__tmp_{i:03}"
        temp_path = os.path.join(target_path, temp_name)
        os.rename(old_path, temp_path)
        temp_mapping[temp_name] = f"{i:03}"

    # 一時名から本番名に変更
    for temp_name, final_name in temp_mapping.items():
        temp_path = os.path.join(target_path, temp_name)
        final_path = os.path.join(target_path, final_name)
        os.rename(temp_path, final_path)
        print(f"✔ Renamed: {temp_name} → {final_name}")

# 使用例（ここを書き換えて実行）
if __name__ == "__main__":
    target_folder = r"C:\Users\HayatoYamagata\Desktop\News\news"  # 対象のフォルダ
    rename_subfolders_to_numbers_in_order(target_folder)
