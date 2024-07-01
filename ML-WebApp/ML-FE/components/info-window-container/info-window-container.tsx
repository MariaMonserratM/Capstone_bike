import { InfoWindow } from "@vis.gl/react-google-maps";
import { useCallback, useEffect, useState } from "react";

interface Station {
  station_id: number;
  lat: number;
  lon: number;
}

function InfoWindowContainer({
  station,
  marker,
  onClose,
}: {
  station: Station;
  marker: google.maps.marker.AdvancedMarkerElement;
  onClose: () => void;
}) {
  const [prediction, setPrediction] = useState<number | null>(null);

  const fetchPrediction = useCallback(
    async function getPrediction() {
      const {
        prediction,
      }: Record<string, Array<number>> = await fetch(`/api/predictor`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ stationId: station.station_id }),
      }).then((res) => res.json());

      setPrediction(prediction[0] ?? null);
    },
    [station.station_id]
  );

  useEffect(() => {
    if (!station.station_id) return;

    fetchPrediction();
  }, [fetchPrediction, station]);

  if (!prediction) return null;

  return (
    <InfoWindow
      anchor={marker}
      onClose={() => {
        setPrediction(null);
        onClose();
      }}
      headerDisabled
    >
      <div className="card card-normal w-96">
        <div className="card-body flex-column justify-center items-center">
          <h2 className="card-title ">Station Id {station.station_id}</h2>
          <div className="divider divider-accent" />
          <p>Availability {prediction * 100}</p>
        </div>
      </div>
    </InfoWindow>
  );
}

export default InfoWindowContainer;
