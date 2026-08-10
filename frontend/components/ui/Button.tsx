import type {
  ButtonHTMLAttributes,
  ReactNode,
} from "react";

interface ButtonProps
  extends ButtonHTMLAttributes<HTMLButtonElement> {
  children: ReactNode;
  variant?: "primary" | "secondary" | "danger";
  loading?: boolean;
}

export default function Button({
  children,
  variant = "primary",
  className = "",
  loading = false,
  disabled,
  ...props
}: ButtonProps) {
  const base =
    "rounded-lg px-4 py-2 text-sm font-medium transition-all disabled:cursor-not-allowed disabled:opacity-50";

  const variants = {
    primary:
      "bg-black text-white hover:bg-gray-800",
    secondary:
      "border border-gray-300 bg-white text-gray-700 hover:bg-gray-50",
    danger:
      "bg-red-600 text-white hover:bg-red-700",
  };

  return (
    <button
      className={`${base} ${variants[variant]} ${className}`}
      disabled={disabled || loading}
      {...props}
    >
      {loading ? "Processing..." : children}
    </button>
  );
}