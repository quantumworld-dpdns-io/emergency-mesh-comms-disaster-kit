import { openDB } from "idb";

const DB_NAME = "mesh-offline";
const STORE = "queue";

export type OfflineItem = { id: string; path: string; body: Record<string, unknown> };

async function db() {
  return openDB(DB_NAME, 1, {
    upgrade(d) {
      if (!d.objectStoreNames.contains(STORE)) d.createObjectStore(STORE, { keyPath: "id" });
    }
  });
}

export async function enqueue(item: OfflineItem) {
  const d = await db();
  await d.put(STORE, item);
}

export async function drain(): Promise<OfflineItem[]> {
  const d = await db();
  const all = await d.getAll(STORE);
  const tx = d.transaction(STORE, "readwrite");
  for (const row of all) await tx.store.delete(row.id);
  await tx.done;
  return all;
}
