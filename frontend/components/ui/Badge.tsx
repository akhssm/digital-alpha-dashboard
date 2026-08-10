interface BadgeProps {
  status: string;
}

export default function Badge({ status }: BadgeProps) {
  const normalizedStatus = status.toUpperCase();

  const statusClasses: Record<string, string> = {
    SUCCESS:
      "bg-emerald-50 text-emerald-700 border border-emerald-200",
    FAILED:
      "bg-red-50 text-red-700 border border-red-200",
    PENDING:
      "bg-amber-50 text-amber-700 border border-amber-200",
  };

  const classes =
    statusClasses[normalizedStatus] ??
    "bg-gray-50 text-gray-700 border border-gray-200";

  return (
    <span
      className={`inline-flex items-center rounded-full px-2.5 py-1 text-xs font-medium ${classes}`}
    >
      {normalizedStatus}
    </span>
  );
}
