import "./SearchBar.css";

export default function SearchBar() {
  return (
    <div className="search-bar">
      <div className="search-inner">
        <input
          className="search-input"
          placeholder="Search for the product you're interested in."
        />
        <button className="search-btn">🔍</button>
      </div>
    </div>
  );
}