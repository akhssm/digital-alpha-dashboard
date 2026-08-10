interface LoadingProps {
  message?: string;
}

export default function Loading({
  message = "Loading...",
}: LoadingProps) {
  return (
    <div className="flex min-h-32 items-center justify-center">
      <div className="flex flex-col items-center gap-3">
        <div
          className="h-8 w-8 animate-spin rounded-full border-4 border-gray-200 border-t-gray-900"
          aria-label="Loading"
        />

        <p className="text-sm text-gray-500">
          {message}
        </p>
      </div>
    </div>
  );
}