// Reusable card for displaying a destination summary on the home and /destinations pages.
import Link from "next/link";
import { MapPin } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import type { PlaceSummary } from "@/lib/api/client";

export function PlaceCard({ place }: { place: PlaceSummary }) {
  return (
    <Link href={`/destinations/${place.slug}`} className="group block h-full">
      <Card className="flex h-full flex-col overflow-hidden transition-shadow hover:shadow-md">
        {/* aspect-[16/10] reserves space before the image loads, preventing layout shift (CLS). */}
        <div className="relative aspect-[16/10] w-full overflow-hidden bg-muted">
          {place.cover_image_url ? (
            <img
              src={place.cover_image_url}
              alt={place.name}
              loading="lazy"
              className="h-full w-full object-cover transition-transform duration-300 group-hover:scale-105"
            />
          ) : (
            <div className="flex h-full items-center justify-center text-sm text-muted-foreground">
              {place.name}
            </div>
          )}
        </div>

        <CardHeader className="pb-2">
          <div className="flex items-center gap-1.5 text-xs font-medium text-muted-foreground">
            <MapPin className="h-3.5 w-3.5 text-primary" />
            <span>{place.region.name}</span>
          </div>
          <CardTitle className="text-lg group-hover:text-primary">{place.name}</CardTitle>
        </CardHeader>

        <CardContent className="flex flex-1 flex-col justify-between gap-4">
          <p className="text-sm text-muted-foreground">{place.short_description}</p>
          <div className="flex flex-wrap gap-1.5">
            {place.categories.map((cat) => (
              <Badge key={cat.slug} variant="secondary">
                {cat.name}
              </Badge>
            ))}
          </div>
        </CardContent>
      </Card>
    </Link>
  );
}

