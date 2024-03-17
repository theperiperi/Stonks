from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Create the engine
engine = create_engine('sqlite:///database.db', echo=True)  # echo=True for logging SQL statements

# Create a base class for declarative class definitions
Base = declarative_base()


# Define the User, Transaction, and Method classes
class User(Base):
    __tablename__ = 'users'

    userid = Column(Integer, primary_key=True)
    password = Column(String)

    transactions = relationship("Transaction", back_populates="user")


class Transaction(Base):
    __tablename__ = 'transactions'

    transactionid = Column(Integer, primary_key=True)
    userid = Column(Integer, ForeignKey('users.userid'))
    methodid = Column(Integer, ForeignKey('methods.methodid'))
    amount = Column(Integer)
    # Add more columns as needed

    user = relationship("User", back_populates="transactions")
    method = relationship("Method", back_populates="transactions")


class Method(Base):
    __tablename__ = 'methods'

    methodid = Column(Integer, primary_key=True)
    name = Column(String)
    # Add more columns as needed

    transactions = relationship("Transaction", back_populates="method")


class DatabaseManager:
    def __init__(self):
        self.engine = create_engine('sqlite:///database.db', echo=True)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def insert_sample_data(self):
        user1 = User(userid=1, password='password123')
        user2 = User(userid=2, password='abc123')
        self.session.add_all([user1, user2])

        method1 = Method(methodid=1, name='Cash')
        method2 = Method(methodid=2, name='Card')
        self.session.add_all([method1, method2])

        transaction1 = Transaction(userid=1, methodid=1, amount=10)
        transaction2 = Transaction(userid=1, methodid=2, amount=100)
        self.session.add_all([transaction1, transaction2])

        self.session.commit()

    def fetch_all_users(self):
        return self.session.query(User).all()

    def fetch_all_transactions(self):
        return self.session.query(Transaction).all()

    def fetch_all_methods(self):
        return self.session.query(Method).all()

    def fetch_all_transactions_for_user(self, userid):
        return self.session.query(Transaction).filter(Transaction.userid == userid).all()

    def fetch_transaction(self, userid: int = None, methodid: int = None):
        query = self.session.query(Transaction)
        if userid:
            query = query.filter(Transaction.userid == userid)
        if methodid:
            query = query.filter(Transaction.methodid == methodid)

        return query.all()

    def __del__(self):
        self.session.close()

    def close(self):
        self.session.close()
