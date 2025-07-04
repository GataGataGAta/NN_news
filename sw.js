const CACHE_NAME = 'fictional-news-cache-v1'; // キャッシュ名。更新時にバージョンを上げる
const assetsToCache = [
  './', // index.html
  './index.html',
  './style.css',
  './scripts/register-sw.js', // 新しく追加したService Worker登録スクリプト
  './manifest.json',
  './images/icon-192x192.png', // manifestに指定されているアイコン
  './images/icon-512x512.png', // manifestに指定されているアイコン
  // ニュース記事のHTMLと画像もキャッシュ対象に含めることを推奨します
  './articles/article_001.html',
  './articles/article_007.html',
  './articles/article_008.html',
  './articles/article_009.html',
  './articles/article_010.html',
  './articles/article_013.html',
  './articles/article_016.html',
  './news/001/img.png',
  './news/007/img.png',
  './news/008/img.png',
  './news/009/img.png',
  './news/010/img.png',
  './news/013/img.png',
  './news/016/img.png'
  // 他のページやリソースも追加してください (例: politics.html, economy.html など)
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        console.log('Opened cache');
        // GitHub Pagesのサブディレクトリ構成に対応するためのパス調整
        const adjustedAssetsToCache = assetsToCache.map(url => {
          // GitHub PagesのURL構造が /your-repo-name/ の場合を考慮
          // Service Workerのスコープ内で相対パスが正しく解決されることが多いですが、
          // 明示的にベースパスを付与する方が安全な場合があります。
          // ただし、sw.jsがルートにあり、assetsToCacheもルートからの相対パスであれば、
          // そのままaddAllで問題ないことが多いです。
          // 念のため、ここでは元のパスのままにしておきます。
          return url;
        });
        return cache.addAll(adjustedAssetsToCache).catch(error => {
            console.error('Failed to cache:', error);
        });
      })
  );
});

self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request)
      .then((response) => {
        if (response) {
          return response;
        }
        return fetch(event.request).then(
          (response) => {
            if (!response || response.status !== 200 || response.type !== 'basic') {
              return response;
            }
            const responseToCache = response.clone();
            caches.open(CACHE_NAME)
              .then((cache) => {
                cache.put(event.request, responseToCache);
              });
            return response;
          }
        );
      })
  );
});

self.addEventListener('activate', (event) => {
  const cacheWhitelist = [CACHE_NAME];
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheWhitelist.indexOf(cacheName) === -1) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});