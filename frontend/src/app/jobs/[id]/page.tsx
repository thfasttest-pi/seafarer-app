"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import { useTelegramInitData } from "@/hooks/useTelegramInitData";
import {
  getJobById,
  type JobDetail,
  UnauthorizedError,
  RateLimitError,
  ApiError,
} from "@/lib/api";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";

type ErrorKind = "unauthorized" | "not_found" | "rate_limit" | "server" | "unknown";

function formatDate(value: string | null | undefined): string {
  if (!value) return "Not specified";
  try {
    const d = new Date(value);
    if (isNaN(d.getTime())) return "Not specified";
    return d.toLocaleDateString();
  } catch {
    return "Not specified";
  }
}

function formatSalary(job: JobDetail | null): string {
  if (!job) return "Not specified";
  const min = job.salary_min;
  const max = job.salary_max;
  const currency = job.salary_currency || "USD";
  if (min != null && max != null && min !== max) {
    return `${min}–${max} ${currency}`;
  }
  if (min != null) return `${min} ${currency}`;
  if (max != null) return `up to ${max} ${currency}`;
  return "Not specified";
}

function displayText(
  value: string | number | boolean | null | undefined,
  options?: { suffix?: string }
): string {
  if (value === null || value === undefined) return "Not specified";
  if (typeof value === "string" && value.trim() === "") return "Not specified";
  const base =
    typeof value === "boolean" ? (value ? "Yes" : "No") : String(value);
  if (options?.suffix) {
    return `${base} ${options.suffix}`;
  }
  return base;
}

function getStatusVariant(status: string | null | undefined):
  | "default"
  | "secondary"
  | "destructive"
  | "outline" {
  if (!status) return "outline";
  const s = status.toLowerCase();
  if (s === "open" || s === "active") return "default";
  if (s === "closed" || s === "filled") return "secondary";
  if (s === "blocked" || s === "cancelled") return "destructive";
  return "outline";
}

export default function JobDetailPage() {
  const params = useParams();
  const rawId = (params?.id ?? "") as string;
  const jobId = Array.isArray(rawId) ? rawId[0] : rawId;

  const { initData, isTelegram, loading: initLoading } = useTelegramInitData();

  const [job, setJob] = useState<JobDetail | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [errorKind, setErrorKind] = useState<ErrorKind | null>(null);

  useEffect(() => {
    if (initLoading) return;
    if (!initData) {
      setErrorKind("unauthorized");
      setErrorMessage(
        "Auth required. Open in Telegram or set NEXT_PUBLIC_DEV_TG_INIT_DATA for local development."
      );
      return;
    }
    if (!jobId) {
      setErrorKind("not_found");
      setErrorMessage("Job not found.");
      return;
    }

    let cancelled = false;
    const fetchJob = async () => {
      setLoading(true);
      setErrorKind(null);
      setErrorMessage(null);
      try {
        const data = await getJobById(jobId, initData);
        if (cancelled) return;
        if (!data || typeof data !== "object") {
          setJob(null);
          setErrorKind("unknown");
          setErrorMessage("Job data is empty or invalid.");
          return;
        }
        setJob(data);
      } catch (e) {
        if (cancelled) return;
        if (e instanceof UnauthorizedError) {
          setErrorKind("unauthorized");
          setErrorMessage(
            "Unauthorized. Open in Telegram or check dev initData."
          );
        } else if (e instanceof RateLimitError) {
          setErrorKind("rate_limit");
          setErrorMessage("Too many requests. Please try again later.");
        } else if (e instanceof ApiError) {
          if (e.statusCode === 404) {
            setErrorKind("not_found");
            setErrorMessage("Job not found.");
          } else if (e.statusCode >= 500) {
            setErrorKind("server");
            setErrorMessage("Server error. Please try again later.");
          } else {
            setErrorKind("unknown");
            setErrorMessage(e.message || "Request failed.");
          }
        } else {
          setErrorKind("unknown");
          setErrorMessage("Something went wrong while loading the job.");
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    };

    fetchJob();

    return () => {
      cancelled = true;
    };
  }, [initLoading, initData, jobId]);

  const showLoading = initLoading || (loading && !job && !errorMessage);

  if (initLoading) {
    return (
      <main className="min-h-screen bg-background px-4 py-6 max-w-[600px] mx-auto">
        <p className="text-muted-foreground">Loading…</p>
      </main>
    );
  }

  if (!initData && !job && errorKind === "unauthorized") {
    return (
      <main className="min-h-screen bg-background px-4 py-6 max-w-[600px] mx-auto">
        <div className="mb-4">
          <Link href="/jobs">
            <Button variant="ghost" size="sm">
              ← Back to jobs
            </Button>
          </Link>
        </div>
        <p className="mb-4 text-sm text-muted-foreground">
          Open this app from Telegram or set NEXT_PUBLIC_DEV_TG_INIT_DATA for
          local development.
        </p>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-background px-4 py-6 max-w-[600px] mx-auto">
      <div className="flex items-center justify-between gap-2 mb-4">
        <Link href="/jobs">
          <Button variant="ghost" size="sm">
            ← Back to jobs
          </Button>
        </Link>
        <span className="text-xs text-muted-foreground">
          {isTelegram ? "Telegram" : "Dev"}
        </span>
      </div>

      {showLoading && (
        <p className="text-muted-foreground mb-4">Loading job…</p>
      )}

      {errorMessage && (
        <div
          className="p-3 mb-4 rounded-md bg-destructive/10 text-destructive text-sm border border-destructive/20"
          role="alert"
        >
          {errorMessage}
        </div>
      )}

      {!showLoading && !errorMessage && !job && (
        <p className="text-muted-foreground text-sm">
          Job data is not available.
        </p>
      )}

      {job && (
        <div className="space-y-4">
          <Card>
            <CardHeader>
              <div className="flex flex-wrap items-center gap-2 mb-2">
                {job.rank && (
                  <Badge variant="secondary" className="font-normal">
                    {job.rank}
                  </Badge>
                )}
                {job.vessel_type && (
                  <Badge variant="outline" className="font-normal">
                    {job.vessel_type}
                  </Badge>
                )}
                {job.status && (
                  <Badge
                    variant={getStatusVariant(job.status)}
                    className="font-normal"
                  >
                    {job.status}
                  </Badge>
                )}
              </div>
              <CardTitle className="text-xl leading-tight">
                {job.title || "Untitled job"}
              </CardTitle>
              <CardDescription>
                Created: {formatDate(job.created_at)}{" "}
                {job.updated_at && (
                  <span className="ml-1">
                    · Updated: {formatDate(job.updated_at)}
                  </span>
                )}
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-sm whitespace-pre-line">
                {job.description && job.description.trim() !== ""
                  ? job.description
                  : "No description provided."}
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-base">Conditions</CardTitle>
              <CardDescription>
                Key terms and requirements for this position.
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-2">
              <div className="flex justify-between text-sm">
                <span className="text-muted-foreground">Salary</span>
                <span className="font-medium">{formatSalary(job)}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-muted-foreground">Contract length</span>
                <span className="font-medium">
                  {displayText(job.contract_months, { suffix: "months" })}
                </span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-muted-foreground">Joining date</span>
                <span className="font-medium">
                  {formatDate(job.joining_date)}
                </span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-muted-foreground">Trading area</span>
                <span className="font-medium">
                  {displayText(job.trading_area)}
                </span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-muted-foreground">
                  Experience required
                </span>
                <span className="font-medium">
                  {displayText(job.experience_required_months, {
                    suffix: "months",
                  })}
                </span>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-base">Vessel & company</CardTitle>
              <CardDescription>
                Additional information when available.
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-2">
              <div className="flex justify-between text-sm">
                <span className="text-muted-foreground">Company</span>
                <span className="font-medium">
                  {displayText(job.company_name)}
                </span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-muted-foreground">Verified company</span>
                <span className="font-medium">
                  {displayText(job.verified_company)}
                </span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-muted-foreground">DWT</span>
                <span className="font-medium">
                  {displayText(job.dwt)}
                </span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-muted-foreground">GRT</span>
                <span className="font-medium">
                  {displayText(job.grt)}
                </span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-muted-foreground">Engine type</span>
                <span className="font-medium">
                  {displayText(job.engine_type)}
                </span>
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </main>
  );
}

