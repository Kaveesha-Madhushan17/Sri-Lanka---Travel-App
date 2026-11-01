// /destinations — Lists all published Sri Lanka places and regions from the backend API.
// (Search and interactive URL filters are added in Phase 2.)
import type { Metadata } from "next";

import { PlaceCard } from "@/components/place-card";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { getCategories, getPlaces, getRegions } from "@/lib/api/client";

export const metadata: Metadata = {
  title: "Destinations in Sri Lanka — Tour Sri",
  description: "Explore beaches, ancient cities, hill country hikes and wildlife parks across Sri Lanka.",
};

export default async function DestinationsPage() {
  const [placesList, regions, categories] = await Promise.all([
    getPlaces({ limit: 50 }),
    getRegions(),
    getCategories(),
  ]);

  return (
    <div className="mx-auto max-w-6xl space-y-12 px-4 py-10">
      <header className="space-y-3">
        <h1 className="text-3xl font-bold tracking-tight text-primary sm:text-4xl">
          Destinations in Sri Lanka
        </h1>
        <p className="max-w-2xl text-muted-foreground">
          Showing {placesList.total} places across {regions.length} regions. Select any destination
          for entry fees, best time to visit, recommended duration and local tips.
        </p>
        <div className="flex flex-wrap gap-2 pt-1">
          {categories.map((cat) => (
            <Badge key={cat.slug} variant="secondary">
              {cat.name}
            </Badge>
          ))}
        </div>
      </header>

      {/* Regions overview */}
      <section aria-labelledby="regions-heading" className="space-y-4">
        <h2 id="regions-heading" className="text-xl font-semibold">
          Regions at a glance
        </h2>
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {regions.map((region) => (
            <Card key={region.slug}>
              <CardHeader className="pb-2">
                <CardTitle className="text-base">{region.name}</CardTitle>
                <p className="text-xs text-muted-foreground">{region.province} Province</p>
              </CardHeader>
              <CardContent className="text-sm text-muted-foreground">
                {region.description}
              </CardContent>
            </Card>
          ))}
        </div>
      </section>

      {/* All destinations grid */}
      <section aria-labelledby="all-places-heading" className="space-y-4">
        <h2 id="all-places-heading" className="text-xl font-semibold">
          All places ({placesList.total})
        </h2>
        <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {placesList.items.map((place) => (
            <PlaceCard key={place.slug} place={place} />
          ))}
        </div>
      </section>
    </div>
  );
}

