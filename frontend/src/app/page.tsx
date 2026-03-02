"use client";

import { useTelegramInitData } from "@/hooks/useTelegramInitData";
import Link from "next/link";

export default function HomePage() {
  const { isTelegram, loading } = useTelegramInitData();

  return (
    <main
      style={{
        padding: "1.5rem",
        maxWidth: "600px",
        margin: "0 auto",
      }}
    >
      <h1 style={{ marginBottom: "1rem", fontSize: "1.5rem" }}>Seafarer App</h1>
      {loading ? (
        <p>Loading…</p>
      ) : (
        <>
          <p
            style={{
              marginBottom: "1rem",
              padding: "0.5rem",
              background: isTelegram ? "#e8f5e9" : "#fff3e0",
              borderRadius: "6px",
              fontSize: "0.9rem",
            }}
          >
            {isTelegram ? "Telegram mode" : "Local dev mode"}
          </p>
          <Link href="/jobs">
            <button type="button" className="primary">
              Open jobs
            </button>
          </Link>
        </>
      )}
    </main>
  );
}
