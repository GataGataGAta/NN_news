// Service Workerの登録
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    // リポジトリ名を含んだ絶対パスを直接指定
    // または、sw.jsがHTMLと同じ階層にあるなら './sw.js'
    const swUrl = '/NN_news/sw.js'; 
    console.log('Attempting to register Service Worker at:', swUrl);

    navigator.serviceWorker.register(swUrl)
      .then(registration => {
        console.log('Service Worker registered with scope: ', registration.scope);
      })
      .catch(error => {
        console.log('Service Worker registration failed: ', error);
      });
  });
}