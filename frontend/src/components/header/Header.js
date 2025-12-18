import { useEffect, useState } from "react";
import SearchBar from "../search/SearchBar";
import "./Header.css";

export default function Header() {
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
  const onScroll = () => {
    setScrolled(window.scrollY > 60);
  };
  window.addEventListener("scroll", onScroll);
  return () => window.removeEventListener("scroll", onScroll);
}, []);

  return (
    <header className={`header ${scrolled ? "scrolled" : ""}`}>
      {/* 상단 라인 */}
      <div className="header-top">
        <div className="logo">
          <span className="dot" />
          LatamBeauty
        </div>

        <div className="header-right">
          <select className="lang">
            <option>ES</option>
            <option>PT</option>
            <option>EN</option>
            <option>KR</option>
          </select>
          <button className="bell">🔔</button>
        </div>
      </div>

      {/* 🔥 SearchBar (여기 한 번만!) */}
      <div className={`search-wrapper ${scrolled ? "center" : ""}`}>
        <SearchBar />
      </div>
    </header>
  );
}