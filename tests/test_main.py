from starlette.testclient import TestClient
from app.main import app

test_app = TestClient(app)
def test_get_health():
    # base_url may be moved to an environment file depending on where it is run
    response = test_app.get("/health")
    correct_dict = {"status": "ok", "service": "devrelay"}
    assert response.status_code == 200 
    assert response.json() == correct_dict
