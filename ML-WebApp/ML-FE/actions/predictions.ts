"use server";

import { PREDICTOR_URL } from "@/utils/url";

export async function fetchStationData(stationId: number) {
  const res = await fetch(PREDICTOR_URL || "", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    //update the corresponding csv fltered row from BE API
    body: JSON.stringify({
      input: [[stationId, 2024, 1, 1, 9, 0.781481, 0.677778, 0.696296, 0.75]],
    }),
  }).then((res) => res.json());

  return res;
}
