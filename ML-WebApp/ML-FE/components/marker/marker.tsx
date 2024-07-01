import {
  AdvancedMarker,
  Pin,
  useAdvancedMarkerRef,
} from "@vis.gl/react-google-maps";
import { memo } from "react";

function MarkerWithInfoWindow({
  position,
  handleMarkerClick,
  stationId,
}: {
  position: { lat: number; lng: number };
  handleMarkerClick: ({
    stationId,
    marker,
  }: {
    stationId: number;
    marker: google.maps.marker.AdvancedMarkerElement;
  }) => void;
  stationId: number;
}) {
  const [markerRef, marker] = useAdvancedMarkerRef();
  console.log("*** rendering marker", stationId);
  return (
    <>
      <AdvancedMarker
        ref={markerRef}
        position={position}
        onClick={() => marker && handleMarkerClick({ stationId, marker })}
      >
        <Pin
          background={"#9933ff"}
          borderColor={"#006425"}
          glyphColor={"#ffccff"}
          scale={0.7}
        />
      </AdvancedMarker>
    </>
  );
}

export default memo(MarkerWithInfoWindow);
