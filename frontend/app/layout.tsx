import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "MoiréForge Dashboard",
  description: "Moiré superlattice SoC — physics, benchmark, API bridge",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
