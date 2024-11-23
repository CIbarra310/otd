// service-worker.js
const CACHE_NAME = 'otd-app-cache-v1';
const urlsToCache = [
  '/',
  '/static/css/style.css',
  '/static/js/scripts.js',
  // Add other assets to cache
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        return cache.addAll(urlsToCache);
      })
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        if (response) {
          return response;
        }
        return fetch(event.request);
      })
  );
});