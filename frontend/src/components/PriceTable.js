import React from "react";

const PriceTable = ({ prices }) => {
  if (!prices || prices.length === 0) {
    return (
      <p style={{ color: "#6b7280", marginTop: "8px" }}>
        아직 등록된 가격 정보가 없습니다.
      </p>
    );
  }

  const sorted = [...prices].sort((a, b) => a.price - b.price);
  const min = sorted[0].price;

  return (
    <div style={{ marginTop: "8px" }}>
      <h3 style={{ fontSize: "18px", marginBottom: "8px" }}>가격 비교</h3>

      <table style={{ width: "100%", borderCollapse: "collapse", fontSize: "14px" }}>
        <thead>
          <tr style={{ backgroundColor: "#f9fafb" }}>
            <th style="padding:8px;text-align:left;">쇼핑몰</th>
            <th style="padding:8px;text-align:right;">가격</th>
            <th style="padding:8px;text-align:center;">링크</th>
          </tr>
        </thead>

        <tbody>
          {sorted.map((item, idx) => (
            <tr key={idx}>
              <td style={{ padding: "8px", borderBottom: "1px solid #eee" }}>
                {item.mall_name}
              </td>

              <td style={{ padding: "8px", borderBottom: "1px solid #eee", textAlign: "right" }}>
                {item.currency} {item.price.toLocaleString()}
                {item.price === min && (
                  <span
                    style={{
                      marginLeft: "8px",
                      padding: "2px 6px",
                      borderRadius: "999px",
                      backgroundColor: "#fee2e2",
                      color: "#b91c1c",
                      fontSize: "11px",
                    }}
                  >
                    최저가
                  </span>
                )}
              </td>

              <td style={{ textAlign: "center", padding: "8px", borderBottom: "1px solid #eee" }}>
                {item.url ? (
                  <a href={item.url} target="_blank" rel="noreferrer" style={{ color: "#2563eb" }}>
                    바로가기
                  </a>
                ) : (
                  "-"
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default PriceTable;
