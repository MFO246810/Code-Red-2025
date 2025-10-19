import React from "react";
import { Navigate } from "react-router-dom";

export default function ProtectedRoute({ children }) {
  const user = localStorage.getItem("user");

  if (!user) {
    // 🚫 Not logged in, redirect
    return <Navigate to="/login" replace />;
  }

  // ✅ Logged in, show content
  return children;
}