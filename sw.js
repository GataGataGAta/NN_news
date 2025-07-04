const CACHE_NAME = 'fictional-news-cache-v1'; // キャッシュ名。サイト更新時にこのバージョンを上げてキャッシュを更新します

// キャッシュするリソースのリスト
// GitHub Pagesのパス (例: /NN_news/) を考慮して、すべてのパスを絶対パスで指定します
const assetsToCache = [
  '/NN_news/', // トップページ (index.html) のルートパス
  '/NN_news/index.html',
  '/NN_news/style.css',
  '/NN_news/scripts/register-sw.js', // Service Worker登録スクリプト
  '/NN_news/manifest.json',
  '/NN_news/images/icon-192x192.png',
  '/NN_news/images/icon-512x512.png',
  // ナビゲーションメニューの各HTMLページ
  '/NN_news/politics.html',
  '/NN_news/economy.html',
  '/NN_news/sports.html',
  '/NN_news/science.html',
  // 注目記事と人気記事のHTMLファイルと画像
  '/NN_news/articles/article_001.html',
  '/NN_news/articles/article_007.html',
  '/NN_news/articles/article_008.html',
  '/NN_news/articles/article_009.html',
  '/NN_news/articles/article_010.html',
  '/NN_news/articles/article_013.html',
  '/NN_news/articles/article_016.html',
  '/NN_news/news/001/img.png',
  '/NN_news/news/007/img.png',
  '/NN_news/news/008/img.png',
  '/NN_news/news/009/img.png',
  '/NN_news/news/010/img.png',
  '/NN_news/news/013/img.png',
  '/NN_news/news/016/img.png'
  // 必要に応じて、他のすべての記事ページや画像などもここに追加してください
];

// Service Workerのインストールイベント
// Service Workerが最初に登録されるときに呼び出され、指定されたファイルをキャッシュします
self.addEventListener('install', (event) => {
  console.log('Service Worker: Install event triggered.');
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        console.log('Service Worker: Caching assets.');
        // キャッシュにすべての指定されたリソースを追加
        return cache.addAll(assetsToCache).catch((error) => {
          console.error('Service Worker: Failed to cache some assets.', error);
        });
      })
      .then(() => self.skipWaiting()) // 新しいService Workerがすぐにアクティブになるようにする
  );
});

// Service Workerのフェッチイベント
// ブラウザがリソースをリクエストするたびに呼び出され、キャッシュから提供するかネットワークから取得するかを決定します
self.addEventListener('fetch', (event) => {
  // GETリクエストのみを処理し、chrome-extension://などのリクエストは無視
  if (event.request.method !== 'GET' || !event.request.url.startsWith('http')) {
    return;
  }

  event.respondWith(
    caches.match(event.request)
      .then((response) => {
        // キャッシュにリソースがあれば、それを返す
        if (response) {
          console.log('Service Worker: Fetching from cache for:', event.request.url);
          return response;
        }

        // キャッシュになければ、ネットワークから取得
        console.log('Service Worker: Fetching from network for:', event.request.url);
        return fetch(event.request)
          .then((response) => {
            // 無効なレスポンス（例: 404, Opaque Response）はキャッシュしない
            if (!response || response.status !== 200 || response.type !== 'basic') {
              return response;
            }

            // 取得したリソースをキャッシュに追加
            const responseToCache = response.clone();
            caches.open(CACHE_NAME)
              .then((cache) => {
                cache.put(event.request, responseToCache);
              });
            return response;
          })
          .catch((error) => {
            console.error('Service Worker: Fetch failed and no cache for:', event.request.url, error);
            // オフライン時にキャッシュにないリソースへのリクエストがあった場合のフォールバック
            // 例えば、オフライン用の代替HTMLページを返すなど
            // return caches.match('/NN_news/offline.html'); // 必要に応じてオフラインページを設定
          });
      })
  );
});

// Service Workerのアクティベートイベント
// 古いキャッシュをクリアし、新しいService Workerが有効になったときに呼び出されます
self.addEventListener('activate', (event) => {
  console.log('Service Worker: Activate event triggered.');
  const cacheWhitelist = [CACHE_NAME]; // 現在有効なキャッシュ名

  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          // ホワイトリストにない（古い）キャッシュを削除
          if (cacheWhitelist.indexOf(cacheName) === -1) {
            console.log('Service Worker: Deleting old cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    })
    .then(() => self.clients.claim()) // すべての既存のクライアント（タブ）をService Workerの制御下に置く
  );
});