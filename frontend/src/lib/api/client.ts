/**
 * Typed API client backed by types generated from FastAPI's OpenAPI schema
 * (`npm run generate:types` -> `src/types/api.d.ts`).
 *
 * Why two URLs?
 * - In the browser (Client Components), requests go to `NEXT_PUBLIC_API_URL`
 *   (`http://localhost:8000` on your host machine).
 * - Inside the `frontend` Docker container (Server Components), `localhost`
 *   would refer to the frontend container itself, so server-side fetches use
 *   `INTERNAL_API_URL` (`http://backend:8000` on the Docker Compose network)
 *   when set, falling back to `NEXT_PUBLIC_API_URL` for local runs.
 */

import type { components } from "@/types/api";

export type HealthResponse = components["schemas"]["HealthResponse"];
export type CategoryOut = components["schemas"]["CategoryOut"];
export type RegionBrief = components["schemas"]["RegionBrief"];
export type RegionOut = components["schemas"]["RegionOut"];
export type ImageOut = components["schemas"]["ImageOut"];
export type PlaceSummary = components["schemas"]["PlaceSummary"];
export type PlaceDetail = components["schemas"]["PlaceDetail"];
export type PlaceList = components["schemas"]["PlaceList"];

const PUBLIC_API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

function getBaseUrl(): string {
  if (typeof window === "undefined") {
    return process.env.INTERNAL_API_URL ?? PUBLIC_API_URL;
  }
  return PUBLIC_API_URL;
}

export class ApiError extends Error {
  constructor(
    public status: number,
    message: string,
  ) {
    super(message);
  }
}

async function apiFetch<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${getBaseUrl()}${path}`, {
    ...init,
    cache: "no-store",
  });
  if (!res.ok) {
    throw new ApiError(res.status, `API ${path} failed with status ${res.status}`);
  }
  return res.json() as Promise<T>;
}

export function getHealth(): Promise<HealthResponse> {
  return apiFetch<HealthResponse>("/api/v1/health");
}

export function getPlaces(params?: { limit?: number; offset?: number }): Promise<PlaceList> {
  const search = new URLSearchParams();
  if (params?.limit !== undefined) search.set("limit", String(params.limit));
  if (params?.offset !== undefined) search.set("offset", String(params.offset));
  const qs = search.toString();
  return apiFetch<PlaceList>(`/api/v1/places${qs ? `?${qs}` : ""}`);
}

export async function getPlaceBySlug(slug: string): Promise<PlaceDetail | null> {
  try {
    return await apiFetch<PlaceDetail>(`/api/v1/places/${encodeURIComponent(slug)}`);
  } catch (err) {
    if (err instanceof ApiError && err.status === 404) {
      return null;
    }
    throw err;
  }
}

export function getRegions(): Promise<RegionOut[]> {
  return apiFetch<RegionOut[]>("/api/v1/regions");
}

export function getCategories(): Promise<CategoryOut[]> {
  return apiFetch<CategoryOut[]>("/api/v1/categories");
}
