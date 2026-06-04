def test_root_redirects_to_static_index(client):
    response = client.get("/", follow_redirects=False)

    assert response.status_code in (302, 307)
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_seeded_data(client):
    response = client.get("/activities")
    payload = response.json()

    assert response.status_code == 200
    assert isinstance(payload, dict)
    assert "Chess Club" in payload
    assert "participants" in payload["Chess Club"]


def test_signup_succeeds_for_existing_activity(client):
    email = "new-student@mergington.edu"
    response = client.post(f"/activities/Chess%20Club/signup?email={email}")
    payload = response.json()

    assert response.status_code == 200
    assert payload["message"] == f"Signed up {email} for Chess Club"


def test_signup_returns_400_for_duplicate_signup(client):
    email = "michael@mergington.edu"
    response = client.post(f"/activities/Chess%20Club/signup?email={email}")
    payload = response.json()

    assert response.status_code == 400
    assert payload["detail"] == "Student already signed up for this activity"

def test_signup_returns_404_for_unknown_activity(client):
    email = "new-student@mergington.edu"
    response = client.post(f"/activities/Unknown%20Club/signup?email={email}")
    payload = response.json()

    assert response.status_code == 404
    assert payload["detail"] == "Activity not found"


def test_unregister_succeeds_for_existing_participant(client):
    email = "michael@mergington.edu"
    response = client.delete(f"/activities/Chess%20Club/participants?email={email}")
    payload = response.json()

    assert response.status_code == 200
    assert payload["message"] == f"Unregistered {email} from Chess Club"


def test_unregister_returns_404_for_missing_participant(client):
    email = "not-enrolled@mergington.edu"
    response = client.delete(f"/activities/Chess%20Club/participants?email={email}")
    payload = response.json()

    assert response.status_code == 404
    assert payload["detail"] == "Participant not found in activity"


def test_unregister_returns_404_for_unknown_activity(client):
    email = "michael@mergington.edu"
    response = client.delete(f"/activities/Unknown%20Club/participants?email={email}")
    payload = response.json()

    assert response.status_code == 404
    assert payload["detail"] == "Activity not found"
