import "./BottomNav.css";

export default function BottomNav() {
  const items = [
    { label: "홈", icon: "🏠" },
    { label: "카테고리", icon: "📁" },
    { label: "지점", icon: "📍" },
    { label: "내 피부", icon: "🧬" },
    { label: "마이", icon: "👤" },
  ];

  return (
    <nav className="bottom-nav">
      {items.map((item) => (
        <button key={item.label} className="bottom-nav-item">
          <div className="icon">{item.icon}</div>
          <div className="label">{item.label}</div>
        </button>
      ))}
    </nav>
  );
}