import React from "react";

export default function IngredientRiskPanel({
  productName,
  riskScore,
  safetyScore,
  riskLevel,
}) {
  return (
    <section
      style={{
        marginTop: 28,
        padding: 20,
        borderRadius: 18,
        background:
          "linear-gradient(180deg, rgba(255,80,80,0.08), rgba(0,0,0,0.2))",
        border: "1px solid rgba(255,255,255,0.12)",
        color: "#fff",
      }}
    >
      {/* 타이틀 */}
      <h3 style={{ fontSize: 17, fontWeight: 800 }}>
        🧪 성분 유해성 분석
      </h3>

      {/* 제품명 */}
      <div style={{ fontSize: 13, opacity: 0.75, marginTop: 6 }}>
        대상 제품: {productName || "-"}
      </div>

      {/* 핵심 요약 */}
      <div
        style={{
          marginTop: 14,
          padding: "12px 14px",
          borderRadius: 12,
          background: "rgba(0,0,0,0.35)",
          border: "1px dashed rgba(255,255,255,0.18)",
        }}
      >
        <div style={{ fontSize: 14 }}>
          현재 위험도 평가:
          <strong style={{ marginLeft: 8 }}>
            {riskLevel || "분석 대기"}
          </strong>
        </div>

        <div style={{ fontSize: 12, opacity: 0.7, marginTop: 6 }}>
          이 평가는 성분 구성, 알려진 유해 성분 DB,
          피부 자극 가능성 지표를 기반으로 계산됩니다.
        </div>
      </div>

      {/* 시각화 자리 (미래 확장) */}
      <div
        style={{
          marginTop: 16,
          height: 60,
          borderRadius: 12,
          background:
            "linear-gradient(90deg, #3ddc97 0%, #f5c542 50%, #ff5c5c 100%)",
          opacity: 0.35,
          position: "relative",
          overflow: "hidden",
        }}
      >
        <div
          style={{
            position: "absolute",
            left: "40%",
            top: 0,
            bottom: 0,
            width: 2,
            background: "#fff",
            opacity: 0.9,
          }}
        />
      </div>

      {/* 설명 문구 */}
      <div style={{ fontSize: 12, opacity: 0.6, marginTop: 10 }}>
        ※ 현재는 MVP 단계입니다.  
        향후 성분별 함유량, 인종·기후·연령별 반응 데이터가
        결합되어 보다 정밀한 분석이 제공됩니다.
      </div>
    </section>
  );
}