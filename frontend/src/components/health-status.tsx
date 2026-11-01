"use client";
// Client Component: runs in the browser, so it calls the backend directly
// (this is a real cross-origin request, which is why the backend enables CORS).

import { useEffect, useState } from "react";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { getHealth, type HealthResponse } from "@/lib/api/client";

type State = { kind: "loading" } | { kind: "ok"; data: HealthResponse } | { kind: "error"; message: string };

function Dot({ good }: { good: boolean }) {
  return <span className={`inline-block h-2.5 w-2.5 rounded-full ${good ? "bg-green-500" : "bg-red-500"}`} />;
}

export function HealthStatus() {
  const [state, setState] = useState<State>({ kind: "loading" });

  useEffect(() => {
    getHealth()
      .then((data) => setState({ kind: "ok", data }))
      .catch((err: Error) => setState({ kind: "error", message: err.message }));
  }, []);

  return (
    <Card className="w-full max-w-sm">
      <CardHeader>
        <CardTitle>System status</CardTitle>
      </CardHeader>
      <CardContent className="space-y-2 text-sm" aria-live="polite">
        {state.kind === "loading" && <p className="text-muted-foreground">Checking backend…</p>}
        {state.kind === "error" && (
          <p className="flex items-center gap-2">
            <Dot good={false} /> Backend unreachable ({state.message})
          </p>
        )}
        {state.kind === "ok" && (
          <>
            <p className="flex items-center gap-2">
              <Dot good /> API: {state.data.status}
            </p>
            <p className="flex items-center gap-2">
              <Dot good={state.data.database === "ok"} /> Database: {state.data.database}
            </p>
          </>
        )}
      </CardContent>
    </Card>
  );
}

