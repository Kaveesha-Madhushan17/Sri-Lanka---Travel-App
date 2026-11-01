"""Load seed data from seed_data/*.json into the database.

Run:  docker compose exec backend python scripts/seed.py

Idempotent = safe to run many times. Rows are matched by `slug`:
existing rows are updated, new ones inserted ("upsert"), never duplicated.

Each place in places.json may have a "TODO: verify" list naming fields whose
values (fees, times) are uncertain and must be checked by hand (PLAN.md rule 6).
"""

import asyncio
import json
from pathlib import Path
from urllib.parse import quote

from sqlalchemy import delete, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import SessionLocal, engine
from app.models import Category, Image, Place, Region, place_categories

SEED_DIR = Path(__file__).resolve().parent.parent / "seed_data"
VERIFY_KEY = "TODO: verify"


def load(name: str) -> list[dict]:
    return json.loads((SEED_DIR / name).read_text(encoding="utf-8"))


async def upsert(db: AsyncSession, model, rows: list[dict]) -> dict[str, int]:
    """INSERT ... ON CONFLICT (slug) DO UPDATE, then return {slug: id}."""
    for row in rows:
        stmt = insert(model).values(**row)
        update_cols = {k: stmt.excluded[k] for k in row if k != "slug"}
        await db.execute(stmt.on_conflict_do_update(index_elements=["slug"], set_=update_cols))
    result = await db.execute(select(model.slug, model.id))
    return dict(result.all())


def placeholder_image(name: str) -> str:
    # Real photos replace these in Phase 4 (Cloudinary upload).
    return f"https://placehold.co/800x500/1f6f4a/ffffff?text={quote(name)}"


async def seed() -> None:
    async with SessionLocal() as db:
        region_ids = await upsert(db, Region, load("regions.json"))
        category_ids = await upsert(db, Category, load("categories.json"))

        to_verify: list[str] = []
        for raw in load("places.json"):
            data = dict(raw)
            # Remove keys that are not columns and translate slugs to ids.
            category_slugs = data.pop("categories")
            verify_fields = data.pop(VERIFY_KEY, [])
            data["region_id"] = region_ids[data.pop("region")]

            place_ids = await upsert(db, Place, [data])
            place_id = place_ids[data["slug"]]

            # Replace the place's categories and images (delete + insert keeps it idempotent).
            await db.execute(delete(place_categories).where(place_categories.c.place_id == place_id))
            await db.execute(
                insert(place_categories),
                [{"place_id": place_id, "category_id": category_ids[c]} for c in category_slugs],
            )
            await db.execute(delete(Image).where(Image.owner_type == "place", Image.owner_id == place_id))
            db.add(
                Image(
                    owner_type="place",
                    owner_id=place_id,
                    url=placeholder_image(data["name"]),
                    alt_text=data["name"],
                    sort_order=0,
                )
            )

            if verify_fields:
                to_verify.append(f"  {data['slug']}: {', '.join(verify_fields)}")

        await db.commit()  # one transaction: all or nothing

    await engine.dispose()
    print(f"Seeded {len(region_ids)} regions, {len(category_ids)} categories, {len(load('places.json'))} places.")
    if to_verify:
        print(f"{VERIFY_KEY} (check these values by hand):")
        print("\n".join(to_verify))


if __name__ == "__main__":
    asyncio.run(seed())

