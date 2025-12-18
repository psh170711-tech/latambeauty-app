import React from "react";

const LANGS = [
  { code: "es", label: "ES" },
  { code: "pt", label: "PT" },
  { code: "en", label: "EN" },
  { code: "ko", label: "KR" },
];

export default function LanguageSelector({ value = "es", onChange }) {
  return (
    <select
      value={value}
      onChange={(e) => onChange?.(e.target.value)}
      style={{
        background: "transparent",
        color: "#fff",
        border: "1px solid rgba(255,255,255,0.15)",
        borderRadius: 8,
        padding: "6px 10px",
        fontSize: 13,
        cursor: "pointer",
      }}
    >
      {LANGS.map((l) => (
        <option key={l.code} value={l.code} style={{ color: "#000" }}>
          {l.label}
        </option>
      ))}
    </select>
  );
}