export interface Transaction {
  id: string;
  timestamp: string;
  merchant: string;
  category: string | null;
  amount: string;
  currency: string;
  status: string;
  payment_method: string;
}

export interface TransactionResponse {
  items: Transaction[];
  total: number;
  skip: number;
  limit: number;
}

export interface Reward {
  id: number;
  name: string;
  description: string;
  coin_cost: number;
  reward_type: string;
  value: number;
  is_active: boolean;
}

export interface CoinBalance {
  id: number;
  balance: number;
}

export interface RedemptionResponse {
  message: string;
  reward_id: number;
  reward_name: string;
  coins_spent: number;
  remaining_balance: number;
}