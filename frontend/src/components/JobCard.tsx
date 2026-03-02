import Link from "next/link";
import type { JobItem } from "@/lib/api";
import {
  Card,
  CardContent,
  CardHeader,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";

interface JobCardProps {
  job: JobItem;
}

function formatDate(dateStr: string | null | undefined): string {
  if (!dateStr) return "—";
  try {
    const d = new Date(dateStr);
    return isNaN(d.getTime()) ? "—" : d.toLocaleDateString();
  } catch {
    return "—";
  }
}

function salarySummary(job: JobItem): string {
  const min = job?.salary_min;
  const max = job?.salary_max;
  const currency = job?.salary_currency ?? "USD";
  if (min != null && max != null && min !== max) {
    return `${min}–${max} ${currency}`;
  }
  if (min != null) return `${min} ${currency}`;
  if (max != null) return `up to ${max} ${currency}`;
  return "Salary not specified";
}

export function JobCard({ job }: JobCardProps) {
  const title = job?.title ?? "—";
  const description =
    job?.description != null && String(job.description).trim() !== ""
      ? String(job.description).slice(0, 120) +
        (String(job.description).length > 120 ? "…" : "")
      : null;
  const created = formatDate(job?.created_at);
  const rank = job?.rank ?? null;
  const vesselType = job?.vessel_type ?? null;
  const salary = salarySummary(job);

  return (
    <Link href={`/jobs/${job?.id ?? "#"}`} className="block">
      <Card
        className={cn(
          "transition-colors hover:bg-muted/50",
          "focus-within:ring-2 focus-within:ring-ring focus-within:ring-offset-2"
        )}
      >
        <CardHeader className="pb-2">
          <div className="flex flex-wrap items-center gap-2">
            {rank && (
              <Badge variant="secondary" className="font-normal">
                {rank}
              </Badge>
            )}
            {vesselType && (
              <Badge variant="outline" className="font-normal">
                {vesselType}
              </Badge>
            )}
          </div>
          <h3 className="text-lg font-semibold leading-tight tracking-tight">
            {title}
          </h3>
          <p className="text-sm text-muted-foreground">{created}</p>
        </CardHeader>
        <CardContent className="pt-0">
          {description && (
            <p className="text-sm text-foreground/90 mb-2 line-clamp-2">
              {description}
            </p>
          )}
          <p className="text-sm font-medium text-muted-foreground">
            {salary}
          </p>
        </CardContent>
      </Card>
    </Link>
  );
}
