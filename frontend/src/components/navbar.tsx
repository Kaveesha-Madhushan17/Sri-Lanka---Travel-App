"use client";
// Client Component because the mobile menu needs state (open/closed).

import Link from "next/link";
import { useState } from "react";
import { Menu, X } from "lucide-react";

import { Button } from "@/components/ui/button";

// Single source of truth for the navigation links (routes come in later phases).
export const NAV_LINKS = [
  { href: "/destinations", label: "Destinations" },
  { href: "/map", label: "Map" },
  { href: "/getting-around", label: "Getting Around" },
  { href: "/culture", label: "Culture" },
  { href: "/essentials", label: "Essentials" },
  { href: "/food", label: "Food" },
  { href: "/plan", label: "Plan a Trip" },
  { href: "/chat", label: "Ask AI" },
];

export function Navbar() {
  const [open, setOpen] = useState(false);

  return (
    <header className="sticky top-0 z-50 border-b bg-background/90 backdrop-blur">
      <nav className="mx-auto flex max-w-6xl items-center justify-between px-4 py-3" aria-label="Main">
        <Link href="/" className="text-lg font-bold text-primary">
          Tour Sri
        </Link>

        {/* Desktop links */}
        <ul className="hidden gap-1 lg:flex">
          {NAV_LINKS.map((l) => (
            <li key={l.href}>
              <Button asChild variant="ghost" size="sm">
                <Link href={l.href}>{l.label}</Link>
              </Button>
            </li>
          ))}
        </ul>

        {/* Mobile menu toggle (mobile-first: visible below the lg breakpoint) */}
        <Button
          variant="ghost"
          size="sm"
          className="lg:hidden"
          aria-label={open ? "Close menu" : "Open menu"}
          aria-expanded={open}
          onClick={() => setOpen(!open)}
        >
          {open ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
        </Button>
      </nav>

      {open && (
        <ul className="border-t px-4 py-2 lg:hidden">
          {NAV_LINKS.map((l) => (
            <li key={l.href}>
              <Link href={l.href} className="block rounded px-2 py-2 hover:bg-accent" onClick={() => setOpen(false)}>
                {l.label}
              </Link>
            </li>
          ))}
        </ul>
      )}
    </header>
  );
}

