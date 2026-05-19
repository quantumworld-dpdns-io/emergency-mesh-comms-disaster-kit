/// <reference lib="webworker" />
import { clientsClaim } from "workbox-core";
import { precacheAndRoute } from "workbox-precaching";
import { registerRoute } from "workbox-routing";
import { StaleWhileRevalidate } from "workbox-strategies";

declare const self: ServiceWorkerGlobalScope & { __WB_MANIFEST: Array<any> };

clientsClaim();
precacheAndRoute(self.__WB_MANIFEST || []);
registerRoute(({ url }) => url.pathname.startsWith("/api/"), new StaleWhileRevalidate());
