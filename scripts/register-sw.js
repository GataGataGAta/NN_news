// Service Workerの登録
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    // GitHub Pagesのパスを考慮してService WorkerのURLを構築する
    // 例: yourusername.github.io/your-repo-name/sw.js
    const basePath = window.location.pathname.split('/')[1]; // リポジトリ名を取得
    const swUrl = `/${basePath}/sw.js`;

    navigator.serviceWorker.register(swUrl)
      .then(registration => {
        console.log('Service Worker registered with scope: ', registration.scope);
      })
      .catch(error => {
        console.log('Service Worker registration failed: ', error);
      });
  });
}