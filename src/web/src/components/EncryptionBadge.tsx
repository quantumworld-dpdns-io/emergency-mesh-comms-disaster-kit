export default function EncryptionBadge({ verified }: { verified: boolean }) {
  return <span className="badge" style={{ background: verified ? "var(--ok)" : "var(--warn)" }}>{verified ? "E2E Verified" : "Unverified"}</span>;
}
