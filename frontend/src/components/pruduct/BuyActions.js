export default function BuyActions({ bestOffer }) {
  if (!bestOffer) return null;

  return (
    <div style={styles.wrapper}>
      <a
        href={bestOffer.url}
        target="_blank"
        rel="noreferrer"
        style={styles.buy}
      >
        최저가로 구매하기
      </a>

      <button style={styles.like}>찜하기</button>
    </div>
  );
}

const styles = {
  wrapper: {
    display: "flex",
    gap: 10,
    marginTop: 14,
  },
  buy: {
    flex: 1,
    padding: "14px 0",
    borderRadius: 14,
    background: "#2dd4bf",
    color: "#000",
    fontWeight: 800,
    textAlign: "center",
    textDecoration: "none",
  },
  like: {
    width: 90,
    borderRadius: 14,
    border: "1px solid rgba(255,255,255,0.15)",
    background: "transparent",
    color: "#fff",
  },
};