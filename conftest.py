from algalon_bot.modules.db.session import Base
from algalon_bot.modules.db import models
from algalon_bot.settings import SQLALCHEMY_DATABASE_SYNC_URI
from sqlalchemy.orm import sessionmaker
from sqlalchemy import event, create_engine
from pydantic import BaseModel
from sqlalchemy_utils import database_exists, create_database, drop_database
import pytest




def get_test_db_url():
    return f"{SQLALCHEMY_DATABASE_SYNC_URI}_bottest"

@pytest.fixture
def test_db():
    """
    Modify the db session to automatically roll back after each test.
    This is to avoid tests affecting the database state of other tests.
    """
    # Connect to the test database
    engine = create_engine(
        get_test_db_url(),
    )

    connection = engine.connect()
    trans = connection.begin()

    # Run a parent transaction that can roll back all changes
    test_session_maker = sessionmaker(
        autocommit=False, autoflush=False, bind=engine
    )
    test_session = test_session_maker()
    test_session.begin_nested()

    @event.listens_for(test_session, "after_transaction_end")
    def restart_savepoint(s, transaction):
        if transaction.nested and not transaction._parent.nested:
            s.expire_all()
            s.begin_nested()

    yield test_session

    # Roll back the parent transaction after the test is complete
    test_session.close()
    trans.rollback()
    connection.close()

@pytest.fixture(scope="session", autouse=True)
def create_test_db():
    """
    Create a test database and use it for the whole test session.
    """

    test_db_url = get_test_db_url().replace('+asyncpg', '')

    # Create the test database
    assert not database_exists(
        test_db_url
    ), "Test database already exists. Aborting tests."
    create_database(test_db_url)
    test_engine = create_engine(test_db_url)
    Base.metadata.create_all(test_engine)

    # Run the tests
    yield

    # Drop the test database
    drop_database(test_db_url)

@pytest.fixture
def test_order(test_db):
    """
    Make a test order in the database
    """
    db_order = models.Order(
        order_id = 6144550810,
        order_direction='buy',
        price=31359.5,
        filled=False,
        creation_timestamp=1626626116059,
    )
    test_db.add(db_order)
    test_db.commit()
    return db_order

@pytest.fixture
def test_order_id(test_order):
    return test_order.order_id

@pytest.fixture
def test_pydantic_order():
    class Order(BaseModel):
        order_id: int
        order_direction: str
        price: float
        order_state: bool
        creation_timestamp: int
    return Order(
        order_id = 6144550810,
        order_direction='buy',
        price=31359.5,
        order_state=False,
        creation_timestamp=1626626116059,
    )

@pytest.fixture
def test_order_model():
    return models.Order