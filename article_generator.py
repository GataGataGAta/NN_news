import os

# 入出力ディレクトリ
TXT_ROOT_DIR = "news"
HTML_OUTPUT_DIR = "articles"
STYLE_PATH = "../style.css"  # 出力HTMLから見たCSSの相対パス

# HTMLテンプレート
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>{title} - 架空ニュース</title>
    <link rel="stylesheet" href="{style_path}">
</head>
<body>
    <header>
        <h1>架空ニュース</h1>
        <nav>
            <ul>
                <li><a href="../index.html">トップ</a></li>
                <li><a href="../politics.html">政治</a></li>
                <li><a href="../economy.html">経済</a></li>
                <li><a href="../sports.html">スポーツ</a></li>
                <li><a href="../science.html">科学</a></li>
            </ul>
        </nav>
    </header>

    <main>
        <section class="main-news">
            <h2>{title}</h2>
            {image_html}
            <p>
{body}
            </p>
        </section>
    </main>

    <footer>
        <p>&copy; 2024 架空ニュース</p>
    </footer>
</body>
</html>
"""

def generate_news_articles():
    os.makedirs(HTML_OUTPUT_DIR, exist_ok=True)

    subfolders = sorted([f for f in os.listdir(TXT_ROOT_DIR) if os.path.isdir(os.path.join(TXT_ROOT_DIR, f))])

    for idx, folder in enumerate(subfolders, 1):
        folder_path = os.path.join(TXT_ROOT_DIR, folder)

        # テキストファイルを探す（1つだけでOKとする）
        txt_files = [f for f in os.listdir(folder_path) if f.endswith(".txt")]
        if not txt_files:
            print(f"⏭ スキップ: {folder} にテキストファイルがありません")
            continue

        txt_path = os.path.join(folder_path, txt_files[0])
        with open(txt_path, "r", encoding="utf-8") as f:
            content = f.read().strip()

        title = content.split("\n")[0].strip() if content else f"記事 {idx}"
        body_html = content.replace("\n", "<br>\n")

        # 画像ファイルを探す（.jpg, .png, .jpeg対応）
        image_file = next((f for f in os.listdir(folder_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))), None)
        image_html = ""
        if image_file:
            image_rel_path = f"../{TXT_ROOT_DIR}/{folder}/{image_file}"
            image_html = f'<img src="{image_rel_path}" alt="記事画像" style="max-width:100%; height:auto;"><br><br>'

        # HTML作成
        html_content = HTML_TEMPLATE.format(
            title=title,
            body=body_html,
            style_path=STYLE_PATH,
            image_html=image_html
        )

        # 出力ファイル
        output_filename = f"article_{idx:03}.html"
        output_path = os.path.join(HTML_OUTPUT_DIR, output_filename)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        print(f"✔ 作成完了: {output_filename} （タイトル: {title}）")

if __name__ == "__main__":
    generate_news_articles()
