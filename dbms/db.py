from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, TIMESTAMP
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from sqlalchemy.sql import func
# Create the engine
engine = create_engine('sqlite:///database.db', echo=True)  # echo=True for logging SQL statements

# Create a base class for declarative class definitions
Base = declarative_base()


# Define the User, Transaction, and Method classes
class User(Base):
    __tablename__ = 'users'

    userid = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)

    transactions = relationship("Transaction", back_populates="user")

    def to_dict(self):
        return {
            "userid": self.userid,
            "username": self.username,
            "password": self.password
        }


class Transaction(Base):
    __tablename__ = 'transactions'

    transactionid = Column(Integer, primary_key=True, autoincrement=True)
    userid = Column(Integer, ForeignKey('users.userid'))
    methodid = Column(Integer, ForeignKey('methods.methodid'))
    amount = Column(Integer)
    timestamp = Column(TIMESTAMP, server_default=func.now(), onupdate=func.current_timestamp())
    # Add more columns as needed

    user = relationship("User", back_populates="transactions")
    method = relationship("Method", back_populates="transactions")

    def to_dict(self):
        return {
            "userid": self.userid,
            "methodid": self.methodid,
            "amount": self.amount,
            "timestamp": self.timestamp
        }


class Method(Base):
    __tablename__ = 'methods'

    methodid = Column(Integer, primary_key=True)
    method_name = Column(String)
    # Add more columns as needed

    transactions = relationship("Transaction", back_populates="method")

    def to_dict(self):
        return {
            "methodid": self.methodid,
            "method_name": self.name
        }


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

    def fetch_user(self, userid):
        return self.session.query(User).filter(User.userid == userid).first()

    def add_user(self, userid, password):
        user = User(userid=userid, password=password)
        self.session.add(user)
        self.session.commit()

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

    def fetch_methods(self, methodid: int = None):
        query = self.session.query(Method)
        if methodid:
            query = query.filter(Method.methodid == methodid)

        return query.all()

    def add_transaction(self, userid, methodid, amount):
        transaction = Transaction(userid=userid, methodid=methodid, amount=amount, timestamp=func.now())
        self.session.add(transaction)
        self.session.commit()

    def __del__(self):
        self.session.close()

    def close(self):
        self.session.close()