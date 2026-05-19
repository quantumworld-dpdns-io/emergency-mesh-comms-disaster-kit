export async function notify(title: string, body: string) {
  if (!("Notification" in window)) return;
  const perm = await Notification.requestPermission();
  if (perm === "granted") new Notification(title, { body });
}
