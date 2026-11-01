// Home page (Server Component): fetches categories and featured places from the FastAPI backend.
import Link from "next/link";
import { Building2, Compass, Landmark, Mountain, PawPrint, Trees, Waves } from "lucide-react";

import { HealthStatus } from "@/components/health-status";
import { PlaceCard } from "@/components/place-card";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { getCategories, getPlaces, type CategoryOut, type PlaceSummary } from "@/lib/api/client";

const CATEGORY_ICONS: Record<string, React.ComponentType<{ className?: string }>> = {
  waves: Waves,
  landmark: Landmark,
  "paw-print": PawPrint,
  mountain: Mountain,
  trees: Trees,
  "building-2": Building2,
};

export default async function HomePage() {
  let categories: CategoryOut[] = [];
  let featuredPlaces: PlaceSummary[] = [];

  try {
    const [cats, placesRes] = await Promise.all([getCategories(), getPlaces({ limit: 6 })]);
    categories = cats;
    featuredPlaces = placesRes.items;
  } catch {
    // If the backend has not been migrated/seeded yet, the page still renders gracefully.
  }

  return (
    <div className="mx-auto max-w-6xl space-y-16 px-4 py-12">
      {/* Hero section */}
      <section className="flex flex-col items-center gap-6 py-8 text-center">
        <h1 className="text-[clamp(2.25rem,1.5rem+3vw,3.5rem)] font-bold tracking-tight text-primary">
          Discover Sri Lanka
        </h1>
        <p className="max-w-2xl text-lg text-muted-foreground">
          Golden beaches, ancient rock fortresses, misty tea country and elephant safaris — with
          accurate fees, best seasons and practical local tips in one place.
        </p>
        <div className="flex flex-wrap justify-center gap-3">
          <Button asChild size="lg">
            <Link href="/destinations">Explore all destinations</Link>
          </Button>
          <Button asChild size="lg" variant="outline">
            <Link href="/plan">Plan a trip</Link>
          </Button>
        </div>
      </section>

      {/* Categories section */}
      {categories.length > 0 && (
        <section aria-labelledby="categories-heading" className="space-y-6">
          <div className="flex items-baseline justify-between">
            <h2 id="categories-heading" className="text-2xl font-bold tracking-tight">
              Browse by interest
            </h2>
          </div>
          <div className="grid grid-cols-2 gap-4 sm:grid-cols-3 lg:grid-cols-6">
            {categories.map((cat) => {
              const Icon = CATEGORY_ICONS[cat.icon] ?? Compass;
              return (
                <Link key={cat.slug} href={`/destinations?category=${cat.slug}`} className="group">
                  <Card className="h-full transition-colors group-hover:border-primary group-hover:bg-accent/50">
                    <CardContent className="flex flex-col items-center gap-2.5 p-5 text-center">
                      <Icon className="h-6 w-6 text-primary" />
                      <span className="text-sm font-medium">{cat.name}</span>
                    </CardContent>
                  </Card>
                </Link>
              );
            })}
          </div>
        </section>
      )}

      {/* Featured places section */}
      <section aria-labelledby="featured-heading" className="space-y-6">
        <div className="flex items-baseline justify-between">
          <div>
            <h2 id="featured-heading" className="text-2xl font-bold tracking-tight">
              Featured destinations
            </h2>
            <p className="text-sm text-muted-foreground">
              Practical guides with entry fees, best visiting times and local advice.
            </p>
          </div>
          <Button asChild variant="outline" size="sm">
            <Link href="/destinations">View all</Link>
          </Button>
        </div>

        {featuredPlaces.length > 0 ? (
          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {featuredPlaces.map((place) => (
              <PlaceCard key={place.slug} place={place} />
            ))}
          </div>
        ) : (
          <Card>
            <CardContent className="p-6 text-sm text-muted-foreground">
              No places loaded yet. Run{" "}
              <code className="rounded bg-muted px-1.5 py-0.5">
                docker compose exec backend alembic upgrade head
              </code>{" "}
              and{" "}
              <code className="rounded bg-muted px-1.5 py-0.5">
                docker compose exec backend python scripts/seed.py
              </code>{" "}
              to populate the database.
            </CardContent>
          </Card>
        )}
      </section>

      {/* Live backend & database health check */}
      <section className="flex justify-center pt-4">
        <HealthStatus />
      </section>
    </div>
  );
}
