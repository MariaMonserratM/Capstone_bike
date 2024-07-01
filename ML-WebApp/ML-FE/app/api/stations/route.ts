import { NextResponse } from "next/server";
import stations from "./stations.json";

interface Station {
  id: number;
  lon: number;
  lat: number;
}
export async function GET() {
  return NextResponse.json(stations);
}
