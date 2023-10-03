import React from 'react';
import {OSMMap} from '../../components/OSMMap';

export function MapView() {
  return (
    <div>
      <h2>Vista del Mapa</h2>
      <OSMMap />
    </div>
  );
}

export default MapView;