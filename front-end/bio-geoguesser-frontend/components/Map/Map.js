"use client";

import 'leaflet/dist/leaflet.css';

import { useState, useEffect } from 'react';
import { MapContainer, TileLayer, Marker, useMapEvents, Popup, CircleMarker, Polyline } from 'react-leaflet';
import L from 'leaflet';

// Fix for default marker icon in Next.js
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
    iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
    iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

function LocationMarker({ onMapClick, guessLocation }) {
  const [position, setPosition] = useState(guessLocation || null);
  
  useEffect(() => {
    setPosition(guessLocation);
  }, [guessLocation]);

  useMapEvents({
    click(e) {
      if (!guessLocation) { // Only allow changing if not already submitted/result view? 
          // Or allow changing guess before submit.
          // The parent controls guessLocation. If we are in result mode, onMapClick might be disabled or handled differently.
          // For now, consistent behavior:
          setPosition(e.latlng);
          if (onMapClick) {
            onMapClick(e.latlng);
          }
      }
    },
  });

  return position === null ? null : (
    <Marker position={position}>
      <Popup>
        You clicked here: <br /> {position.lat.toFixed(5)}, {position.lng.toFixed(5)}
      </Popup>
    </Marker>
  );
}

function Map({ onMapClick, guessLocation, actualLocations, closestLocation }) {
    return (
        <MapContainer center={[51.505, -0.09]} zoom={2} scrollWheelZoom={true} style={{ height: "100vh", width: "100%" }}>
            <TileLayer
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            />
            <LocationMarker onMapClick={onMapClick} guessLocation={guessLocation} />
            
            {actualLocations && actualLocations.map((loc, idx) => (
                <CircleMarker 
                    key={idx} 
                    center={[loc.lat, loc.lng]} 
                    pathOptions={{ color: 'red', fillColor: 'red', fillOpacity: 0.5, radius: 5 }}
                >
                   <Popup>Sighting {idx + 1}</Popup>
                </CircleMarker>
            ))}

            {closestLocation && guessLocation && (
                <Polyline 
                    positions={[
                        [guessLocation.lat, guessLocation.lng],
                        [closestLocation.lat, closestLocation.lng]
                    ]}
                    pathOptions={{ color: 'blue', dashArray: '10, 10' }}
                />
            )}
        </MapContainer>
    );
}


export default Map;