import os

# 入出力ディレクトリ
TXT_DIR = "news"
HTML_DIR = "articles"
STYLE_PATH = "../style.css"  # HTMLから見たCSSの相対パス

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
                <li><a href="#">政治</a></li>
                <li><a href="#">経済</a></li>
                <li><a href="#">スポーツ</a></li>
                <li><a href="#">テクノロジー</a></li>
            </ul>
        </nav>
    </header>

    <main>
        <section class="main-news">
            <h2>{title}</h2>
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

def generate_html_files():
    if not os.path.exists(HTML_DIR):
        os.makedirs(HTML_DIR)

    txt_files = sorted([f for f in os.listdir(TXT_DIR) if f.endswith(".txt")])
    if not txt_files:
        print("テキストファイルが見つかりません。")
        return

    for idx, filename in enumerate(txt_files, 1):
        txt_path = os.path.join(TXT_DIR, filename)
        with open(txt_path, "r", encoding="utf-8") as f:
            content = f.read().strip()

        # タイトルは最初の行（またはファイル名）
        title = content.split("\n")[0].strip() if content else filename.replace(".txt", "")

        # 改行を <br> に変換
        body_html = content.replace("\n", "<br>\n")

        # HTML生成
        html = HTML_TEMPLATE.format(
            title=title,
            body=body_html,
            style_path=STYLE_PATH
        )

        # 出力ファイル名（article_001.html の形式）
        output_filename = f"article_{idx:03}.html"
        output_path = os.path.join(HTML_DIR, output_filename)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)

        print(f"✔ 生成完了: {output_filename}")

if __name__ == "__main__":
    generate_html_files()
