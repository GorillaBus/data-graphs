import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './ui/App';

// 1. Crear una raíz
const root = ReactDOM.createRoot(document.getElementById('root')!);

// 2. Renderizar tu App en esa raíz
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);