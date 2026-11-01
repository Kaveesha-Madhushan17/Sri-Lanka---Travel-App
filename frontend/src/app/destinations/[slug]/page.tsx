// /destinations/[slug] — Detail page for a single place (e.g. /destinations/sigiriya).
// Shows entry fees (foreign USD & local LKR), best time to visit, duration and tips.
import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { ArrowLeft, Calendar, Clock, Lightbulb, MapPin, Ticket } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { getPlaceBySlug } from "@/lib/api/client";

type Props = {
  params: Promise<{ slug: string }>;
};

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { slug } = await params;
  const place = await getPlaceBySlug(slug);
  if (!place) {
    return { title: "Place not found — Tour Sri" };
  }
  return {
    title: `${place.name} — Tour Sri`,
    description: place.short_description,
  };
}

function formatForeignFee(usd: number | null): string {
  if (usd === null) return "Free / check locally";
  if (usd === 0) return "Free";
  return `$${usd} USD`;
}

function formatLocalFee(lkr: number | null): string {
  if (lkr === null) return "Free / check locally";
  if (lkr === 0) return "Free";
  return `LKR ${lkr.toLocaleString()}`;
}

export default async function PlaceDetailPage({ params }: Props) {
  const { slug } = await params;
  const place = await getPlaceBySlug(slug);

  if (!place) {
    notFound();
  }

  return (
    <article className="mx-auto max-w-4xl space-y-8 px-4 py-10">
      <div>
        <Button asChild variant="ghost" size="sm">
          <Link href="/destinations">
            <ArrowLeft className="h-4 w-4" />
            Back to destinations
          </Link>
        </Button>
      </div>

      {/* Header */}
      <header className="space-y-3">
        <div className="flex flex-wrap items-center gap-2 text-sm text-muted-foreground">
          <span className="inline-flex items-center gap-1 font-medium text-primary">
            <MapPin className="h-4 w-4" />
            {place.region.name}
          </span>
          <span>·</span>
          <span>
            {place.latitude.toFixed(4)}° N, {place.longitude.toFixed(4)}° E
          </span>
        </div>

        <h1 className="text-3xl font-bold tracking-tight sm:text-4xl">{place.name}</h1>
        <p className="text-lg text-muted-foreground">{place.short_description}</p>

        <div className="flex flex-wrap gap-2 pt-1">
          {place.categories.map((cat) => (
            <Badge key={cat.slug}>{cat.name}</Badge>
          ))}
          {place.tags.map((tag) => (
            <Badge key={tag} variant="outline">
              #{tag}
            </Badge>
          ))}
        </div>
      </header>

      {/* Cover image with fixed aspect-ratio to prevent layout shift */}
      {place.cover_image_url && (
        <div className="aspect-[16/9] w-full overflow-hidden rounded-xl border bg-muted">
          <img
            src={place.cover_image_url}
            alt={place.images[0]?.alt_text ?? place.name}
            className="h-full w-full object-cover"
          />
        </div>
      )}

      {/* Practical info cards: fees, best time, duration */}
      <section aria-label="Practical information" className="grid gap-4 sm:grid-cols-3">
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="flex items-center gap-2 text-sm font-semibold text-muted-foreground">
              <Ticket className="h-4 w-4 text-primary" />
              Entry fee
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-1 text-sm">
            <p>
              <span className="font-medium">Foreign:</span>{" "}
              {formatForeignFee(place.entry_fee_foreign_usd)}
            </p>
            <p className="text-muted-foreground">
              <span className="font-medium text-foreground">Local:</span>{" "}
              {formatLocalFee(place.entry_fee_local_lkr)}
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="flex items-center gap-2 text-sm font-semibold text-muted-foreground">
              <Calendar className="h-4 w-4 text-primary" />
              Best time to visit
            </CardTitle>
          </CardHeader>
          <CardContent className="text-sm">{place.best_time_to_visit}</CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="flex items-center gap-2 text-sm font-semibold text-muted-foreground">
              <Clock className="h-4 w-4 text-primary" />
              Recommended duration
            </CardTitle>
          </CardHeader>
          <CardContent className="text-sm">
            {place.recommended_duration_hours
              ? `About ${place.recommended_duration_hours} hours`
              : "Flexible"}
          </CardContent>
        </Card>
      </section>

      {/* Full description */}
      <section className="space-y-3">
        <h2 className="text-xl font-semibold">About {place.name}</h2>
        <p className="leading-relaxed text-foreground/90">{place.description}</p>
      </section>

      {/* Practical tips */}
      {place.tips.length > 0 && (
        <Card className="border-primary/30 bg-accent/40">
          <CardHeader className="pb-2">
            <CardTitle className="flex items-center gap-2 text-lg">
              <Lightbulb className="h-5 w-5 text-primary" />
              Practical tips
            </CardTitle>
          </CardHeader>
          <CardContent>
            <ul className="list-disc space-y-1.5 pl-5 text-sm">
              {place.tips.map((tip) => (
                <li key={tip}>{tip}</li>
              ))}
            </ul>
          </CardContent>
        </Card>
      )}
    </article>
  );
}

