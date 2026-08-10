"use client";

import { Coins, CreditCard } from "lucide-react";

interface HeaderProps {
  balance: number;
}

export default function Header({
  balance,
}: HeaderProps) {
  return (
    <header className="border-b border-gray-200 bg-white">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-4 sm:px-6 lg:px-8">
        {/* Logo / Brand */}
        <div className="flex items-center gap-3">
          <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-black text-white">
            <CreditCard size={18} />
          </div>

          <div>
            <h1 className="text-lg font-bold text-gray-900">
              AlphaPay
            </h1>

            <p className="hidden text-xs text-gray-500 sm:block">
              Payments & Rewards
            </p>
          </div>
        </div>

        {/* Coin Balance */}
        <div className="flex items-center gap-2 rounded-full bg-amber-50 px-3 py-2 sm:px-4">
          <Coins
            size={18}
            className="text-amber-600"
          />

          <span className="text-sm font-semibold text-gray-900">
            {balance.toLocaleString()} coins
          </span>
        </div>
      </div>
    </header>
  );
}