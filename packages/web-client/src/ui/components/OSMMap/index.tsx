import React, { useRef, useState, useEffect } from "react";
import { MapContainer, Marker, Popup, TileLayer, GeoJSON, Polyline } from "react-leaflet";
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import './style.css';

L.Icon.Default.mergeOptions({
  iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
  iconUrl: require('leaflet/dist/images/marker-icon.png'),
  shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
});

const defaultPosition = {
  lat: 35.7407872,
  lng: 51.4375991,
  zoom: 13
};

type MarkerData = {
  position: [number, number],
  label: string,
}
const markersData: MarkerData[] = [
  { position: [35.745, 51.430], label: 'A' },
  { position: [35.735, 51.440], label: 'B' }
];

export const OSMMap: React.FC = () => {
  const markersRef = useRef<{[key: string]: any}>({});
  const [areaFeatures, setAreaFeatures] = useState<any>(null);
  const [markersReady, setMarkersReady] = useState<boolean>(false);

  const fetchFeatures = async () => {
    const markerA = markersRef.current['A'].getLatLng();
    const markerB = markersRef.current['B'].getLatLng();

    try {
      const response = await fetch(`http://127.0.0.1:5000/api/find-path/${markerA.lat}/${markerA.lng}/${markerB.lat}/${markerB.lng}`);
      
      if (!response.ok) {
        const errorData = await response.json();
        alert(`Error: ${errorData.error}`);
        return;
      }
      
      const data = await response.json();
      
      setAreaFeatures(data.path);      

    } catch (error) {

      alert("An error occurred while requesting data");
    }
  };

  const handleDragEnd = async (label: string) => {
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
            draggable={true}
            eventHandlers={{ dragend: () => handleDragEnd(marker.label) }}>
            <Popup>This is position {marker.label}</Popup>
          </Marker>
        ))}
        {
            areaFeatures &&
                <Polyline
                    key='path'
                    positions={areaFeatures.map((node: any) => [node.lat, node.lon])}
                    color="blue"
                />
        }
      </MapContainer>
    </div>
  );
}
