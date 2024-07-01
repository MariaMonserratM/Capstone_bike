"use client";
import { Map } from "@vis.gl/react-google-maps";
import MapContainer from "./map-container";
import { useCallback, useEffect, useState, memo } from "react";
import MarkerWithInfoWindow from "../marker";
import InfoWindowContainer from "../info-window-container";

interface Station {
  station_id: number;
  lat: number;
  lon: number;
}

export default function MapClient() {
  const [data, setData] = useState<Station[]>([]);
  const [selectedStation, setSelectedStation] = useState<{
    station: Station;
    marker: google.maps.marker.AdvancedMarkerElement;
  } | null>(null);

  const ucFetchData = useCallback(async () => {
    try {
      const res = await fetch("/api/stations");
      if (!res.ok) {
        throw new Error("Network response was not ok");
      }
      const data: Station[] = await res.json();
      if (!data) throw new Error("No data");
      setData(data);
    } catch (error) {}
  }, []);

  useEffect(() => {
    ucFetchData();
  }, [ucFetchData]);

  useEffect(() => {
    const listener = (e: KeyboardEvent) => {
      if (e.key === "Escape") {
        setSelectedStation(null);
      }
    };
    window.addEventListener("keydown", listener);

    return () => {
      window.removeEventListener("keydown", listener);
    };
  }, []);

  const ucHanleMarkerClick = useCallback(
    ({
      stationId,
      marker,
    }: {
      stationId: number;
      marker: google.maps.marker.AdvancedMarkerElement;
    }) => {
      const foundSelectedStation = data.find(
        (station) => station.station_id === stationId
      );
      if (!foundSelectedStation) return;
      setSelectedStation({ station: foundSelectedStation, marker });
    },
    [data]
  );

  if (data.length === 0) {
    return null;
  }

  return (
    <MapContainer>
      <Map
        streetViewControl
        defaultCenter={{ lat: 41.38879, lng: 2.15899 }}
        defaultZoom={13}
        gestureHandling={"cooperative"}
        mapId="DEMO_MAP_ID"
        controlSize={24}
        className="relative h-screen w-full "
        onClick={() => {
          setSelectedStation(null);
        }}
      >
        <MemoList data={data} handleMarkerClick={ucHanleMarkerClick} />
        {selectedStation && (
          <InfoWindowContainer
            station={selectedStation.station}
            marker={selectedStation.marker}
            onClose={() => setSelectedStation(null)}
          />
        )}
      </Map>
    </MapContainer>
  );
}

const MemoizedMarkerList = ({
  data,
  handleMarkerClick,
}: {
  data: Station[];
  handleMarkerClick: (args: {
    stationId: number;
    marker: google.maps.marker.AdvancedMarkerElement;
  }) => void;
}) => {
  return (
    <>
      {data.map(({ station_id, lat, lon }) => (
        <MarkerWithInfoWindow
          key={station_id}
          position={{ lat, lng: lon }}
          handleMarkerClick={handleMarkerClick}
          stationId={station_id}
        />
      ))}
    </>
  );
};

const MemoList = memo(MemoizedMarkerList);
