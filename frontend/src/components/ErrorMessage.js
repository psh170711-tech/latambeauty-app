import React from "react";

const ErrorMessage = ({ message }) => {
  if (!message) return null;

  return (
    <div
      style={{
        marginTop: "8px",
        marginBottom: "16px",
        padding: "10px 12px",
        borderRadius: "8px",
        backgroundColor: "#fef2f2",
        color: "#b91c1c",
        fontSize: "14px",
      }}
    >
      {message}
    </div>
  );
};

export default ErrorMessage;
