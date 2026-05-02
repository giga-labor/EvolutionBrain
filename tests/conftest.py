import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.db.session import get_db
from app.main import app
from app.core.config import Settings


@pytest.fixture(scope="function")
def db_engine(tmp_path):
    db_file = tmp_path / "test_evobrain.db"
    db_url = f"sqlite:///{db_file}"
    engine = create_engine(db_url, connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture(scope="function")
def client(db_engine, tmp_path):
    db_file = tmp_path / "test_evobrain.db"
    db_url = f"sqlite:///{db_file}"
    TestSession = sessionmaker(bind=db_engine, autoflush=False, autocommit=False)

    def override_get_db():
        db = TestSession()
        try:
            yield db
        finally:
            db.close()

    def override_get_settings() -> Settings:
        return Settings(database_url=db_url)

    app.dependency_overrides[get_db] = override_get_db

    import app.api.routes.system as _system_route
    _orig = _system_route.get_settings
    _system_route.get_settings = override_get_settings

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()
    _system_route.get_settings = _orig
