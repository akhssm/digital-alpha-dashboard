from app.database.connection import Base, engine
from app.models.transaction import Transaction
from app.models.reward import Reward


def init_db():
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")


if __name__ == "__main__":
    init_db()