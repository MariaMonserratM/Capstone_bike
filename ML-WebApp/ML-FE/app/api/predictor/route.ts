import { fetchStationData } from "@/actions/predictions";
import { NextResponse } from "next/server";

export async function POST(req: Request) {
  const { stationId } = await req.json();
  // Fetch data based on the stationId
  const data = await fetchStationData(stationId);

  return NextResponse.json(data);
}


