from PIL import Image

# 192x192アイコン作成
img192 = Image.new('RGBA', (192, 192), (30, 144, 255, 255))  # ドッジャーブルー背景
img192.save('icons/icon-192.png')

# 512x512アイコン作成
img512 = Image.new('RGBA', (512, 512), (30, 144, 255, 255))  # 同じ色で大きいサイズ
img512.save('icons/icon-512.png')
