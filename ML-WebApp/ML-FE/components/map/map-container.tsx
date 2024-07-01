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
        "AIzaSyBHkxfS_nlqW0_KMpd8H-t47y6GRc_MTEk"
      }
    >
      {children}
    </APIProvider>
  );
}