/**
 * WhatToWatch Service Worker
 *
 * Provides basic offline support by caching the application's shell.
 */

const CACHE_NAME = "whattowatch-v1";

const APP_SHELL = [
    "/",
    "/static/css/base.css",
    "/static/js/script.js",
    "/static/images/favicon/android-chrome-192x192.png",
    "/static/images/favicon/android-chrome-512x512.png",
    "/static/images/favicon/apple-touch-icon.png"
];

self.addEventListener("install", event => {
    event.waitUntil(
        caches.open(CACHE_NAME).then(cache => cache.addAll(APP_SHELL))
    );

    self.skipWaiting();
});

self.addEventListener("activate", event => {
    event.waitUntil(
        caches.keys().then(keys =>
            Promise.all(
                keys
                    .filter(key => key !== CACHE_NAME)
                    .map(key => caches.delete(key))
            )
        )
    );

    self.clients.claim();
});

self.addEventListener("fetch", event => {
    if (event.request.method !== "GET") return;

    event.respondWith(
        caches.match(event.request).then(response => {
            return response || fetch(event.request);
        })
    );
});