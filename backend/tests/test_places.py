"""Tests for /places, /regions and /categories (data comes from conftest.py)."""


def test_list_places_returns_only_published(client):
    res = client.get("/api/v1/places")
    assert res.status_code == 200
    body = res.json()
    slugs = [p["slug"] for p in body["items"]]
    assert slugs == ["mirissa", "sigiriya"]  # ordered by name; draft excluded
    assert body["total"] == 2


def test_list_places_includes_region_categories_and_cover(client):
    sigiriya = next(p for p in client.get("/api/v1/places").json()["items"] if p["slug"] == "sigiriya")
    assert sigiriya["region"]["slug"] == "cultural-triangle"
    assert [c["slug"] for c in sigiriya["categories"]] == ["culture-heritage"]
    assert sigiriya["cover_image_url"] == "https://example.com/s.jpg"


def test_list_places_pagination(client):
    body = client.get("/api/v1/places", params={"limit": 1, "offset": 1}).json()
    assert [p["slug"] for p in body["items"]] == ["sigiriya"]
    assert body["total"] == 2
    assert body["limit"] == 1 and body["offset"] == 1


def test_list_places_rejects_invalid_limit(client):
    assert client.get("/api/v1/places", params={"limit": 0}).status_code == 422
    assert client.get("/api/v1/places", params={"limit": 101}).status_code == 422


def test_get_place_detail(client):
    res = client.get("/api/v1/places/sigiriya")
    assert res.status_code == 200
    place = res.json()
    # The "done when" criteria of Phase 1: fees, best time, duration and tips.
    assert place["entry_fee_foreign_usd"] == 36.0
    assert place["entry_fee_local_lkr"] == 100
    assert place["best_time_to_visit"] == "Early morning"
    assert place["recommended_duration_hours"] == 3.0
    assert place["tips"] == ["Start early"]
    assert place["images"][0]["url"] == "https://example.com/s.jpg"


def test_get_place_not_found(client):
    assert client.get("/api/v1/places/does-not-exist").status_code == 404


def test_unpublished_place_is_hidden(client):
    assert client.get("/api/v1/places/draft-place").status_code == 404


def test_list_regions(client):
    regions = client.get("/api/v1/regions").json()
    assert [r["slug"] for r in regions] == ["cultural-triangle", "south-coast"]
    assert regions[1]["best_months"] == [12, 1, 2, 3]


def test_list_categories(client):
    categories = client.get("/api/v1/categories").json()
    assert {c["slug"] for c in categories} == {"beach", "culture-heritage"}

