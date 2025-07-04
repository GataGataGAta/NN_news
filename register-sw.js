// register-sw.js (index.html と同じディレクトリに配置)

if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    // Service Worker (sw.js) が index.html と同じディレクトリにある場合、
    // パスは './sw.js' でOKです。GitHub Pagesのサブディレクトリも自動的に考慮されます。
    navigator.serviceWorker.register('./sw.js')
      .then(registration => {
        console.log('Service Worker registered with scope: ', registration.scope);
      })
      .catch(error => {
        console.log('Service Worker registration failed: ', error);
      });
  });
}