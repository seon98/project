def test_organization_crud_flow(client):
    # Create
    resp = client.post("/organizations/", json={"name": "Org A", "description": "Test org"})
    assert resp.status_code == 201, resp.text
    data = resp.json()
    org_id = data["id"]
    assert data["name"] == "Org A"

    # List
    resp = client.get("/organizations/")
    assert resp.status_code == 200
    items = resp.json()
    assert any(item["id"] == org_id for item in items)

    # Get
    resp = client.get(f"/organizations/{org_id}")
    assert resp.status_code == 200
    assert resp.json()["name"] == "Org A"

    # Update
    resp = client.put(f"/organizations/{org_id}", json={"name": "Org A2"})
    assert resp.status_code == 200
    assert resp.json()["name"] == "Org A2"

    # Delete
    resp = client.delete(f"/organizations/{org_id}")
    assert resp.status_code == 204

    # Get after delete
    resp = client.get(f"/organizations/{org_id}")
    assert resp.status_code == 404
