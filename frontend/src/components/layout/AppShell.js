import React from "react";
import "./AppShell.css";

export default function AppShell({ header, children, bottomNav }) {
  return (
    <div style={{ minHeight: "100vh", display: "flex", flexDirection: "column" }}>
      {header}
      <main style={{ flex: 1, padding: "16px" }}>{children}</main>
      {bottomNav}
    </div>
  );
}