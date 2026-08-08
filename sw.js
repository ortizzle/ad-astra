/* Ad Astra service worker.
   Bump CACHE_VERSION on every deploy — mobile Chrome caches aggressively and a
   stale shell is the #1 cause of "my fix isn't showing up". */
const CACHE_VERSION = 'ad-astra-v56';
const SHELL = [
  './',
  './index.html',
  './manifest.json',
  './icon.svg'
];
/* prototype.html is a design comparison page, deliberately not cached. */

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE_VERSION)
      .then(c => c.addAll(SHELL))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(k => k !== CACHE_VERSION).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  const url = new URL(e.request.url);

  // Never cache API traffic — Anthropic and GitHub must always hit the network.
  if (url.hostname === 'api.anthropic.com' || url.hostname === 'api.github.com') return;
  if (e.request.method !== 'GET') return;

  // Network-first for the app shell so a deploy lands on next load;
  // fall back to cache when offline.
  if (url.origin === self.location.origin) {
    e.respondWith(
      fetch(e.request)
        .then(res => {
          const copy = res.clone();
          caches.open(CACHE_VERSION).then(c => c.put(e.request, copy));
          return res;
        })
        .catch(() => caches.match(e.request).then(r => r || caches.match('./index.html')))
    );
    return;
  }

  // Cache-first for CDN assets (fonts).
  e.respondWith(
    caches.match(e.request).then(hit => hit || fetch(e.request).then(res => {
      const copy = res.clone();
      caches.open(CACHE_VERSION).then(c => c.put(e.request, copy));
      return res;
    }).catch(() => hit))
  );
});
