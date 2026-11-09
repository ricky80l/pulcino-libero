// Aiutante del gioco come app: serve a Chrome per poterlo installare sulla schermata Home.
// Non tiene niente in memoria: ogni richiesta va in rete come sempre.
self.addEventListener('install', function () { self.skipWaiting(); });
self.addEventListener('activate', function (e) { e.waitUntil(self.clients.claim()); });
self.addEventListener('fetch', function (e) { e.respondWith(fetch(e.request)); });
