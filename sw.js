/* Ad Astra service worker.
   Bump CACHE_VERSION on every deploy — mobile Chrome caches aggressively and a
   stale shell is the #1 cause of "my fix isn't showing up". */
/* The page asks the waiting worker to take over when she taps Refresh —
   never automatically, so a mid-round quiz is never yanked. */
self.addEventListener('message', e => { if(e.data === 'skip') self.skipWaiting(); });
const CACHE_VERSION = 'ad-astra-v95';
const SHELL = [
  './',
  './index.html',
  './manifest.json',
  './icon.svg',
  './fonts/fraunces.woff2',
  './fonts/fraunces-italic.woff2',
  './fonts/jakarta.woff2'
];
/* prototype.html is a design comparison page, deliberately not cached. */

/* No skipWaiting here, deliberately (changed alongside the update bar): a new
   worker used to take over mid-session the moment it installed, which is how a
   half-loaded old page ends up mixing old code with new caches. It now WAITS —
   the page shows "a new version is ready", and taking over happens when she
   taps Refresh (the 'skip' message below) or on the next cold start. */
self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE_VERSION)
      .then(c => c.addAll(SHELL))
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

  // Cache-first for CDN assets (fonts) — and the network try is BOUNDED.
  // A hung connection here (captive portal, flaky proxy) used to hold the
  // pending stylesheet open forever, which blocks every <script> after it:
  // the app simply never finished loading. Four seconds, then fail cleanly —
  // the system font stack takes over and the app runs.
  e.respondWith(
    caches.match(e.request).then(hit => {
      if(hit) return hit;
      const ctl = new AbortController();
      const t = setTimeout(() => ctl.abort(), 4000);
      return fetch(e.request, {signal: ctl.signal}).then(res => {
        clearTimeout(t);
        const copy = res.clone();
        caches.open(CACHE_VERSION).then(c => c.put(e.request, copy));
        return res;
      }).catch(() => { clearTimeout(t); return Response.error(); });
    })
  );
});
