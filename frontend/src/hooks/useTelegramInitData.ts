"use client";

import { useState, useEffect } from "react";
import { isTelegramWebApp, getInitData, ready, expand } from "@/lib/tma";

/**
 * Returns initData for API client and Telegram mode flag.
 * - In Telegram: uses WebApp.initData.
 * - Local dev: can use NEXT_PUBLIC_DEV_TG_INIT_DATA (optional env) to mock auth.
 *   Only set in .env.local for development; never in production.
 */
export function useTelegramInitData(): {
  initData: string;
  isTelegram: boolean;
  loading: boolean;
} {
  const [initData, setInitData] = useState("");
  const [isTelegram, setIsTelegram] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const isTg = isTelegramWebApp();
    setIsTelegram(isTg);
    let data = "";
    if (isTg) {
      data = getInitData();
      ready();
      expand();
    } else {
      const dev = process.env.NEXT_PUBLIC_DEV_TG_INIT_DATA;
      if (dev && typeof dev === "string") data = dev;
    }
    setInitData(data);
    setLoading(false);
  }, []);

  return { initData, isTelegram, loading };
}
