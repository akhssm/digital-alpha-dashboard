const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

export async function getCoinBalance() {
  const response = await fetch(
    `${API_BASE_URL}/coin-balance/`
  );

  if (!response.ok) {
    throw new Error("Failed to fetch coin balance");
  }

  return response.json();
}

export async function getRewards() {
  const response = await fetch(
    `${API_BASE_URL}/rewards/`
  );

  if (!response.ok) {
    throw new Error("Failed to fetch rewards");
  }

  return response.json();
}

export async function getTransactions(params: {
  skip?: number;
  limit?: number;
  category?: string;
  status?: string;
  search?: string;
  start_date?: string;
  end_date?: string;
  min_amount?: number;
  max_amount?: number;
  sort_by?: "timestamp" | "amount";
  sort_order?: "asc" | "desc";
}) {
  const searchParams = new URLSearchParams();

  if (params.skip !== undefined)
    searchParams.set("skip", String(params.skip));

  if (params.limit !== undefined)
    searchParams.set("limit", String(params.limit));

  if (params.category)
    searchParams.set("category", params.category);

  if (params.status)
    searchParams.set("status", params.status);

  if (params.search)
    searchParams.set("search", params.search);

  if (params.start_date)
    searchParams.set("start_date", params.start_date);

  if (params.end_date)
    searchParams.set("end_date", params.end_date);

  if (params.min_amount !== undefined)
    searchParams.set("min_amount", String(params.min_amount));

  if (params.max_amount !== undefined)
    searchParams.set("max_amount", String(params.max_amount));

  if (params.sort_by)
    searchParams.set("sort_by", params.sort_by);

  if (params.sort_order)
    searchParams.set("sort_order", params.sort_order);

  const response = await fetch(
    `${API_BASE_URL}/transactions/?${searchParams.toString()}`
  );

  if (!response.ok) {
    throw new Error("Failed to fetch transactions");
  }

  return response.json();
}

export async function redeemReward(rewardId: number) {
  const response = await fetch(
    `${API_BASE_URL}/rewards/${rewardId}/redeem`,
    {
      method: "POST",
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail || "Failed to redeem reward"
    );
  }

  return data;
}