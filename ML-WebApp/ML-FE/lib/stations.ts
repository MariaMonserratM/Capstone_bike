import "server-only";

export async function getStations() {
  const res = await fetch("/api/stations", {});

  return res.json();
}
