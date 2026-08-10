"use client";

import { Transaction } from "@/lib/api";
import Card from "../ui/Card";

interface TransactionTableProps {
  transactions: Transaction[];
}

export default function TransactionTable({
  transactions,
}: TransactionTableProps) {
  return (
    <Card>
      {/* Header */}
      <div>
        <h3 className="text-lg font-semibold text-gray-900">
          Recent Transactions
        </h3>

        <p className="mt-1 text-sm text-gray-500">
          Latest payment activity
        </p>
      </div>

      {/* Table */}
      <div className="mt-6 overflow-x-auto">
        <table className="w-full text-left text-sm">
          <thead className="bg-gray-50 text-gray-500">
            <tr>
              <th className="px-5 py-3 font-medium">
                Merchant
              </th>

              <th className="px-5 py-3 font-medium">
                Category
              </th>

              <th className="px-5 py-3 font-medium">
                Amount
              </th>

              <th className="px-5 py-3 font-medium">
                Status
              </th>

              <th className="px-5 py-3 font-medium">
                Date
              </th>
            </tr>
          </thead>

          <tbody className="divide-y divide-gray-100">
            {transactions.length === 0 ? (
              <tr>
                <td
                  colSpan={5}
                  className="px-5 py-8 text-center text-gray-500"
                >
                  No transactions found.
                </td>
              </tr>
            ) : (
              transactions.map((transaction) => (
                <tr
                  key={transaction.id}
                  className="hover:bg-gray-50"
                >
                  <td className="px-5 py-4 font-medium text-gray-900">
                    {transaction.merchant}
                  </td>

                  <td className="px-5 py-4 text-gray-600">
                    {transaction.category || "—"}
                  </td>

                  <td className="px-5 py-4 font-medium text-gray-900">
                    {transaction.currency}{" "}
                    {Number(transaction.amount).toLocaleString()}
                  </td>

                  <td className="px-5 py-4">
                    <span
                      className={`rounded-full px-2.5 py-1 text-xs font-medium ${
                        transaction.status === "SUCCESS"
                          ? "bg-green-100 text-green-700"
                          : transaction.status === "FAILED"
                          ? "bg-red-100 text-red-700"
                          : "bg-yellow-100 text-yellow-700"
                      }`}
                    >
                      {transaction.status}
                    </span>
                  </td>

                  <td className="px-5 py-4 text-gray-500">
                    {new Date(
                      transaction.timestamp
                    ).toLocaleDateString()}
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </Card>
  );
}