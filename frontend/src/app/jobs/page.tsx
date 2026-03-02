"use client";

import { useState, useEffect, useCallback } from "react";
import Link from "next/link";
import { useSearchParams, useRouter, usePathname } from "next/navigation";
import { useTelegramInitData } from "@/hooks/useTelegramInitData";
import { getJobs, type JobItem } from "@/lib/api";
import {
  UnauthorizedError,
  RateLimitError,
  ApiError,
} from "@/lib/api";
import { JobCard } from "@/components/JobCard";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

const LIMIT = 10;

const RANK_OPTIONS = [
  { value: "any", label: "Any rank" },
  { value: "AB", label: "AB" },
  { value: "Chief Officer", label: "Chief Officer" },
  { value: "Captain", label: "Captain" },
  { value: "Chief Engineer", label: "Chief Engineer" },
  { value: "2nd Officer", label: "2nd Officer" },
  { value: "2nd Engineer", label: "2nd Engineer" },
  { value: "3rd Officer", label: "3rd Officer" },
  { value: "Cook", label: "Cook" },
  { value: "Oiler", label: "Oiler" },
  { value: "OS", label: "OS" },
];

const VESSEL_TYPE_OPTIONS = [
  { value: "any", label: "Any vessel" },
  { value: "Bulk Carrier", label: "Bulk Carrier" },
  { value: "Tanker", label: "Tanker" },
  { value: "Container", label: "Container" },
  { value: "General Cargo", label: "General Cargo" },
  { value: "Chemical Tanker", label: "Chemical Tanker" },
  { value: "LNG", label: "LNG" },
  { value: "LPG", label: "LPG" },
  { value: "Offshore", label: "Offshore" },
];

function useFiltersFromUrl() {
  const searchParams = useSearchParams();
  return {
    search: searchParams.get("search") ?? "",
    rank: searchParams.get("rank") ?? "",
    vessel_type: searchParams.get("vessel_type") ?? "",
  };
}

export default function JobsPage() {
  const router = useRouter();
  const pathname = usePathname();
  const searchParams = useSearchParams();
  const { initData, isTelegram, loading: initLoading } = useTelegramInitData();
  const filters = useFiltersFromUrl();

  const [items, setItems] = useState<JobItem[]>([]);
  const [nextCursor, setNextCursor] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [loadMoreLoading, setLoadMoreLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const updateUrl = useCallback(
    (updates: { search?: string; rank?: string; vessel_type?: string }) => {
      const p = new URLSearchParams(searchParams);
      if (updates.search !== undefined) {
        if (updates.search.trim()) p.set("search", updates.search.trim());
        else p.delete("search");
      }
      if (updates.rank !== undefined) {
        if (updates.rank) p.set("rank", updates.rank);
        else p.delete("rank");
      }
      if (updates.vessel_type !== undefined) {
        if (updates.vessel_type) p.set("vessel_type", updates.vessel_type);
        else p.delete("vessel_type");
      }
      const qs = p.toString();
      router.replace(qs ? `${pathname}?${qs}` : pathname);
    },
    [pathname, router, searchParams]
  );

  const fetchPage = useCallback(
    async (cursor: string | null, append: boolean) => {
      if (!initData) {
        setError("Auth required. Open in Telegram or set NEXT_PUBLIC_DEV_TG_INIT_DATA.");
        return;
      }
      if (append) setLoadMoreLoading(true);
      else setLoading(true);
      setError(null);
      try {
        const res = await getJobs(
          {
            limit: LIMIT,
            cursor,
            search: filters.search || undefined,
            rank: filters.rank || undefined,
            vessel_type: filters.vessel_type || undefined,
          },
          initData
        );
        const list = res?.items ?? [];
        const next = res?.next_cursor ?? null;
        if (append) {
          setItems((prev) => [...prev, ...list]);
        } else {
          setItems(list);
        }
        setNextCursor(next);
      } catch (e) {
        if (e instanceof UnauthorizedError) {
          setError("Unauthorized. Open in Telegram or check dev initData.");
        } else if (e instanceof RateLimitError) {
          setError("Too many requests. Try again later.");
        } else if (e instanceof ApiError) {
          setError(e.message || "Request failed.");
        } else {
          setError("Something went wrong.");
        }
      } finally {
        setLoading(false);
        setLoadMoreLoading(false);
      }
    },
    [initData, filters.search, filters.rank, filters.vessel_type]
  );

  useEffect(() => {
    if (initLoading || !initData) return;
    setItems([]);
    setNextCursor(null);
    fetchPage(null, false);
  }, [initLoading, initData, filters.search, filters.rank, filters.vessel_type, fetchPage]);

  const loadMore = () => {
    if (nextCursor && !loadMoreLoading) fetchPage(nextCursor, true);
  };

  const handleSearchChange = (value: string) => {
    updateUrl({ search: value });
  };

  const handleRankChange = (value: string) => {
    updateUrl({ rank: value });
  };

  const handleVesselTypeChange = (value: string) => {
    updateUrl({ vessel_type: value });
  };

  if (initLoading) {
    return (
      <main className="min-h-screen bg-background px-4 py-6 max-w-[600px] mx-auto">
        <p className="text-muted-foreground">Loading…</p>
      </main>
    );
  }

  if (!initData) {
    return (
      <main className="min-h-screen bg-background px-4 py-6 max-w-[600px] mx-auto">
        <p className="mb-4 text-muted-foreground">
          Open this app from Telegram or set NEXT_PUBLIC_DEV_TG_INIT_DATA for local dev.
        </p>
        <Link href="/" className="text-primary underline-offset-4 hover:underline">
          Back
        </Link>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-background px-4 py-6 max-w-[600px] mx-auto">
      <div className="flex items-center gap-2 mb-4">
        <Link
          href="/"
          className="text-primary underline-offset-4 hover:underline text-sm"
        >
          ← Back
        </Link>
        <span className="text-sm text-muted-foreground">
          {isTelegram ? "Telegram" : "Dev"}
        </span>
      </div>

      <h1 className="text-xl font-semibold mb-4">Jobs</h1>

      <div className="space-y-3 mb-6">
        <Input
          type="search"
          placeholder="Search by title or description…"
          value={filters.search}
          onChange={(e) => handleSearchChange(e.target.value)}
          className="w-full"
          aria-label="Search jobs"
        />
        <div className="grid grid-cols-2 gap-2">
          <Select value={filters.rank || "any"} onValueChange={(v) => handleRankChange(v === "any" ? "" : v)}>
            <SelectTrigger className="w-full" aria-label="Filter by rank">
              <SelectValue placeholder="Rank" />
            </SelectTrigger>
            <SelectContent>
              {RANK_OPTIONS.map((opt) => (
                <SelectItem key={opt.value} value={opt.value}>
                  {opt.label}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
          <Select value={filters.vessel_type || "any"} onValueChange={(v) => handleVesselTypeChange(v === "any" ? "" : v)}>
            <SelectTrigger className="w-full" aria-label="Filter by vessel type">
              <SelectValue placeholder="Vessel type" />
            </SelectTrigger>
            <SelectContent>
              {VESSEL_TYPE_OPTIONS.map((opt) => (
                <SelectItem key={opt.value} value={opt.value}>
                  {opt.label}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>
      </div>

      {error && (
        <div
          className="p-3 mb-4 rounded-md bg-destructive/10 text-destructive text-sm border border-destructive/20"
          role="alert"
        >
          {error}
        </div>
      )}

      {loading ? (
        <p className="text-muted-foreground">Loading jobs…</p>
      ) : items.length === 0 && !error ? (
        <p className="text-muted-foreground">No jobs found.</p>
      ) : (
        <>
          <ul className="space-y-3 list-none p-0 m-0">
            {items.map((job) => (
              <li key={job.id}>
                <JobCard job={job} />
              </li>
            ))}
          </ul>
          {nextCursor && (
            <Button
              type="button"
              variant="outline"
              className="w-full mt-4"
              onClick={loadMore}
              disabled={loadMoreLoading}
            >
              {loadMoreLoading ? "Loading…" : "Load more"}
            </Button>
          )}
        </>
      )}
    </main>
  );
}
