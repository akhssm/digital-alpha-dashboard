"use client";

import { useEffect, useState } from "react";

import Header from "@/components/ui/Header";
import Card from "@/components/ui/Card";
import TransactionTable from "@/components/transactions/TransactionTable";

import {
  getCoinBalance,
  getTransactions,
  Transaction,
} from "@/lib/api";

interface CoinBalanceResponse {
  balance: number;
}

interface TransactionResponse {
  items: Transaction[];
  total: number;
  skip: number;
  limit: number;
}

export default function Home() {
  const [balance, setBalance] = useState<number>(0);

  const [transactions, setTransactions] =
    useState<Transaction[]>([]);

  const [loading, setLoading] =
    useState<boolean>(true);

  const [transactionsLoading, setTransactionsLoading] =
    useState<boolean>(true);

  const [error, setError] =
    useState<string>("");

  const [transactionsError, setTransactionsError] =
    useState<string>("");

  // Load coin balance
  useEffect(() => {
    async function loadBalance(): Promise<void> {
      try {
        const data: CoinBalanceResponse =
          await getCoinBalance();

        setBalance(data.balance);
      } catch (error: unknown) {
        console.error(error);
        setError("Unable to load coin balance");
      } finally {
        setLoading(false);
      }
    }

    loadBalance();
  }, []);

  // Load transactions
  useEffect(() => {
    async function loadTransactions(): Promise<void> {
      try {
        setTransactionsLoading(true);

        const data: TransactionResponse =
          await getTransactions({
            skip: 0,
            limit: 10,
          });

        setTransactions(data.items);
      } catch (error: unknown) {
        console.error(error);

        setTransactionsError(
          "Unable to load transactions"
        );
      } finally {
        setTransactionsLoading(false);
      }
    }

    loadTransactions();
  }, []);

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <Header balance={balance} />

      <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
        {/* Page heading */}
        <div className="mb-8">
          <h2 className="text-2xl font-bold text-gray-900">
            Financial Dashboard
          </h2>

          <p className="mt-1 text-sm text-gray-500">
            Track your transactions, spending and rewards.
          </p>
        </div>

        {/* Summary cards */}
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">

          {/* Reward Balance */}
          <Card>
            <p className="text-sm text-gray-500">
              Reward Balance
            </p>

            <p className="mt-2 text-3xl font-bold text-gray-900">
              {loading
                ? "..."
                : balance.toLocaleString()}
            </p>

            <p className="mt-1 text-xs text-gray-500">
              Available coins
            </p>
          </Card>

          {/* Transactions */}
          <Card>
            <p className="text-sm text-gray-500">
              Transactions
            </p>

            <p className="mt-2 text-3xl font-bold text-gray-900">
              {transactionsLoading
                ? "..."
                : transactions.length}
            </p>

            <p className="mt-1 text-xs text-gray-500">
              Recent transactions
            </p>
          </Card>

          {/* Total Spending */}
          <Card>
            <p className="text-sm text-gray-500">
              Total Spending
            </p>

            <p className="mt-2 text-3xl font-bold text-gray-900">
              ₹ —
            </p>

            <p className="mt-1 text-xs text-gray-500">
              Analytics coming next
            </p>
          </Card>
        </div>

        {/* Coin balance error */}
        {error && (
          <p className="mt-4 text-sm text-red-600">
            {error}
          </p>
        )}

        {/* Transaction error */}
        {transactionsError && (
          <p className="mt-4 text-sm text-red-600">
            {transactionsError}
          </p>
        )}

        {/* Transactions */}
        <section className="mt-8">
          {transactionsLoading ? (
            <Card>
              <p className="text-sm text-gray-500">
                Loading transactions...
              </p>
            </Card>
          ) : transactionsError ? (
            <Card>
              <p className="text-sm text-red-600">
                {transactionsError}
              </p>
            </Card>
          ) : (
            <TransactionTable
              transactions={transactions}
            />
          )}
        </section>
      </main>
    </div>
  );
}