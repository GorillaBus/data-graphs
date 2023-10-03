import React, { useState } from "react";
import { MapContainer, Marker, Popup, TileLayer, Circle } from "react-leaflet";
import * as turf from '@turf/turf';
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

const markerA: [number, number] = [35.745, 51.430];
const markerB: [number, number] = [35.735, 51.440];

export const OSMMap = () => {
  const pointA = turf.point(markerA);
  const pointB = turf.point(markerB);
  const distance = turf.distance(pointA, pointB) * 1000; // Convertido a metros
  
  const midpoint = turf.midpoint(pointA, pointB);
  const circleCenter = midpoint.geometry.coordinates as [number, number];
  const circleRadius = distance * 2;

  console.log("circleRadius", circleRadius)

  console.log("circleCenter", circleCenter)


  const position: [number, number] = [defaultPosition.lat, defaultPosition.lng];

  const [loc, setLoc] = useState<[number, number]>([
    defaultPosition.lat,
    defaultPosition.lng
  ]);
  return (
    <div>
        <MapContainer className="map" center={loc} zoom={defaultPosition.zoom}>
          <TileLayer
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          />
          <Marker position={markerA}>
            <Popup>
              This is position A
            </Popup>
          </Marker>

          <Marker position={markerB}>
            <Popup>
              This is position B
            </Popup>
          </Marker>
          <Circle center={circleCenter} radius={circleRadius} />
        </MapContainer>
    </div>);
}
