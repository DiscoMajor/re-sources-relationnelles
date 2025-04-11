const staticCacheName = 're-sources-cache-v1';

const filesToCache = [
    '/',
    '/static/css/main.css',
    '/static/css/styles.css',
    '/static/pwa/offline.html'
];

// Installation du service worker
self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(staticCacheName)
        .then(cache => {
            return cache.addAll(filesToCache);
        })
    );
});

// Activation du service worker
self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames
                    .filter(cacheName => cacheName.startsWith('re-sources-'))
                    .filter(cacheName => cacheName !== staticCacheName)
                    .map(cacheName => caches.delete(cacheName))
            );
        })
    );
});

// Interception des requêtes
self.addEventListener('fetch', event => {
    event.respondWith(
        caches.match(event.request)
            .then(response => {
                return response || fetch(event.request)
                    .catch(() => {
                        return caches.match('/static/pwa/offline.html');
                    });
            })
    );
});