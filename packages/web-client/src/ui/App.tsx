import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import MapView from './views/MapView';

export function App() {
  return (
    <Router>
      <div>
        <Routes>
          <Route path="/map" element={<MapView />} />
          <Route path="/" element={<h2>Bienvenido a la aplicación</h2>} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
