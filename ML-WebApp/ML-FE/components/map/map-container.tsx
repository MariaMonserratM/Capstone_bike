"use client";

import { APIProvider } from "@vis.gl/react-google-maps";

export default function MapContainer({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <APIProvider
      apiKey={
        process.env.GOOGLE_MAPS_API_KEY ||
        ""
      }
    >
      {children}
    </APIProvider>
  );
}
