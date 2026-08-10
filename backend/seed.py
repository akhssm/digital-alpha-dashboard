import json
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path

from sqlalchemy import delete

from app.database.connection import SessionLocal
from app.models.transaction import Transaction


BASE_DIR = Path(__file__).resolve().parent.parent
JSON_FILE = BASE_DIR / "transactions.json"


def parse_timestamp(value):
    if isinstance(value, (int, float)):
        return datetime.fromtimestamp(
            value / 1000,
            tz=timezone.utc
        )

    if isinstance(value, str):
        value = value.strip()

        # Unix timestamp in milliseconds
        if value.isdigit():
            return datetime.fromtimestamp(
                int(value) / 1000,
                tz=timezone.utc
            )

        # ISO 8601 datetime
        if "T" in value:
            if value.endswith("Z"):
                value = value[:-1] + "+00:00"

            return datetime.fromisoformat(value)

        # DD/MM/YYYY HH:MM:SS
        try:
            return datetime.strptime(
                value,
                "%d/%m/%Y %H:%M:%S"
            ).replace(tzinfo=timezone.utc)
        except ValueError:
            pass

        # YYYY-MM-DD
        try:
            return datetime.strptime(
                value,
                "%Y-%m-%d"
            ).replace(tzinfo=timezone.utc)
        except ValueError:
            pass

    raise ValueError(f"Unsupported timestamp format: {value}")


def load_transactions():
    with open(JSON_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def seed_transactions():
    transactions = load_transactions()

    print(f"Found {len(transactions)} transactions in JSON.")

    db = SessionLocal()

    try:
        # Remove existing records so the script can be safely rerun
        db.execute(delete(Transaction))

        batch = []

        for item in transactions:
            transaction = Transaction(
                id=item["id"],
                timestamp=parse_timestamp(item["timestamp"]),
                merchant=item["merchant"],
                category=item.get("category"),
                amount=Decimal(str(item["amount"])),
                currency=item["currency"],
                status=item["status"],
                payment_method=item["payment_method"],
            )

            batch.append(transaction)

            if len(batch) >= 1000:
                db.add_all(batch)
                db.flush()
                batch.clear()

        if batch:
            db.add_all(batch)

        db.commit()

        print(f"Successfully seeded {len(transactions)} transactions.")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_transactions()