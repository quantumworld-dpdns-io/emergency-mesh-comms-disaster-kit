export default function EmergencyPanel() {
  return <div className="card"><h3>Emergency</h3><button onClick={() => navigator.vibrate?.([80, 40, 80])}>SOS Broadcast</button></div>;
}
