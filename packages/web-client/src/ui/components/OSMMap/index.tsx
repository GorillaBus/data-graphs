import React, { useRef, useState, useEffect } from "react";
import L from 'leaflet';
import { TNode } from "@web-client/domain/definitions/gis"
import { MapContainer, Marker, TileLayer, Polyline } from "react-leaflet";

import 'leaflet/dist/leaflet.css';
import './style.css';

L.Icon.Default.mergeOptions({
  iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
  iconUrl: require('leaflet/dist/images/marker-icon.png'),
  shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
});

const defaultPosition = {
  lat: -34.7833,
  lng: -58.4000,
  zoom: 17
};

type MarkerData = {
  position: [number, number],
  label: string,
}
const markersData: MarkerData[] = [
  { position: [-34.7833, -58.4002], label: 'A' },
  { position: [-34.7839, -58.4038], label: 'B' }
];

export const OSMMap: React.FC = () => {
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const markersRef = useRef<{[key: string]: any}>({});
  const [areaFeatures, setAreaFeatures] = useState<TNode[]>(null);
  const [markersReady, setMarkersReady] = useState<boolean>(false);

  
  const fetchFeatures = async () => {
    setIsLoading(true);
    setError(null);

    const markerA = markersRef.current['A'].getLatLng();
    const markerB = markersRef.current['B'].getLatLng();
    try {
        const response = await fetch(`http://127.0.0.1:5000/api/find-path/${markerA.lat}/${markerA.lng}/${markerB.lat}/${markerB.lng}`);        
        if (!response.ok) {
            const errorData = await response.json();
            setError(errorData.error);
            return;
        }
        
        const data = await response.json();
        setAreaFeatures(data.path);      

    } catch (error) {
        setError("An error occurred while requesting data");
    } finally {
      setIsLoading(false);
  }

    setIsLoading(false);
  };

  const handleDragEnd = async () => {
    await fetchFeatures();
  };

  useEffect(() => {
    if (markersReady) {
      fetchFeatures();
    }
  }, [markersReady]);

  const handleMarkerRef = (label: string, ref: any) => {
    markersRef.current[label] = ref;
    if (markersRef.current.A && markersRef.current.B) {
      setMarkersReady(true);
    }
  }

  return (
    <div style={{ height: "100vh", width: "100%" }}>
      <MapContainer
        className="map"
        center={defaultPosition}
        zoom={defaultPosition.zoom}
        style={{ height: "100%", width: "100%" }}
        dragging={!isLoading}
        zoomControl={!isLoading}
      >

        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        />

        {markersData.map(marker => (
            <Marker
                key={marker.label}
                ref={ref => handleMarkerRef(marker.label, ref)}
                position={marker.position}
                draggable={!isLoading}
                eventHandlers={{ dragend: () => handleDragEnd() }}
            >
            </Marker>
        ))}

        {/* Path polyline */}
        {
          areaFeatures &&
              <Polyline
                  key='path'
                  positions={areaFeatures.map((node: TNode) => [node.lat, node.lon])}
                  color="blue"
              />
        }
      </MapContainer>

      {/* Loader */}
      {isLoading && (
            <div style={{
                position: 'absolute',
                top: '50%',
                left: '50%',
                transform: 'translate(-50%, -50%)',
                zIndex: 1000,
                backgroundColor: 'rgba(255, 255, 255, 0.8)',
                padding: '20px',
                borderRadius: '8px',
            }}>
                Loading...
            </div>
        )}

      {/* Errors */}
      {error && (
          <div style={{
              position: 'absolute',
              top: '50%',
              left: '50%',
              transform: 'translate(-50%, -50%)',
              zIndex: 1000,
              backgroundColor: 'rgba(255, 255, 255, 0.8)',
              padding: '20px',
              borderRadius: '8px',
          }}
          onClick={() => setError(null)}>
              {error}
          </div>
      )}
    </div>
  );
}
