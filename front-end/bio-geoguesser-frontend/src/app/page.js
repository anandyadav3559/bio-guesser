"use client";

import { useState } from "react";
import { Luckiest_Guy } from "next/font/google";

import Card from "../../components/Card";
import Map from "../../components/Map";

const luckiestGuy = Luckiest_Guy({
  weight: "400",
  subsets: ["latin"],
});

export default function Home() {
  const [gameData, setGameData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [isGuessing, setIsGuessing] = useState(false);
  const [guessLocation, setGuessLocation] = useState(null);
  const [score, setScore] = useState(null);

  const handleStartGame = async () => {
    setLoading(true);
    setIsGuessing(false); 
    setGuessLocation(null);
    setScore(null);
    try {
      const response = await fetch(`${process.env.API_URL}/start_game`);

      if (!response.ok) {
        throw new Error("Failed to fetch game data");
      }
      const data = await response.json();
      setGameData(data);
    } catch (error) {
      console.error("Error starting game:", error);
      alert("Failed to start game. Is the backend running?");
    } finally {
      setLoading(false);
    }
  };

  const handleGuessSubmit = async () => {
    if (!guessLocation) {
      alert("Please click on the map to select a location first!");
      return;
    }

    try {
      const response = await fetch(
        `${process.env.API_URL}/get_score?lat=${guessLocation.lat}&lng=${guessLocation.lng}`
      );
      if (!response.ok) {
        throw new Error("Failed to calculate score");
      }
      const data = await response.json();
      setScore(data);
    } catch (error) {
      console.error("Error calculating score:", error);
      alert("Failed to submit guess. Try again.");
    }
  };

  return (
    <main
      className={`min-h-screen flex flex-col items-center justify-center bg-blue-600 text-white ${luckiestGuy.className}`}
    >
      <div className="flex flex-col items-center gap-8 w-full px-4">
        {gameData ? (
           isGuessing ? (
             <div className="fixed inset-0 z-50 bg-black">
               <div className="relative h-full w-full">
                  <Map 
                    onMapClick={setGuessLocation} 
                    guessLocation={guessLocation}
                    actualLocations={score?.all_sightings}
                    closestLocation={score?.closest_sighting}
                  /> 
                  
                  {score ? (
                    <div className="absolute inset-0 z-[2000] flex items-end justify-center pointer-events-none pb-12">
                      <div className="pointer-events-auto flex flex-col items-center gap-4 rounded-3xl bg-black/80 p-8 text-center border-4 border-yellow-400 shadow-[0_0_50px_rgba(250,204,21,0.5)] animate-in slide-in-from-bottom-10 fade-in duration-500 max-w-2xl w-full mx-4">
                        <h2 className="text-5xl text-yellow-400 drop-shadow-md">SCORE: {score.score}</h2>
                        
                        <div className="flex gap-8 text-xl text-gray-200">
                           <p>Distance: <span className="text-yellow-400 font-bold">{score.distance_km} km</span></p>
                           <p>Accuracy: <span className="text-green-400 font-bold">{score.score > 800 ? "AMAZING!" : score.score > 500 ? "GOOD JOB!" : "NICE TRY!"}</span></p>
                        </div>
                        <button
                          onClick={() => {
                            handleStartGame();
                          }}
                          className="mt-2 rounded-full bg-blue-500 px-10 py-3 text-xl font-bold text-white shadow-[0_6px_0_rgb(29,78,216)] transition active:translate-y-2 active:shadow-none hover:bg-blue-400 border-4 border-blue-700 hover:scale-105"
                        >
                          PLAY AGAIN
                        </button>
                      </div>
                    </div>
                  ) : (
                    <button 
                        onClick={handleGuessSubmit}
                        className="absolute bottom-12 left-1/2 -translate-x-1/2 rounded-full bg-green-500 px-12 py-4 text-3xl font-bold text-white shadow-[0_6px_0_rgb(21,128,61)] transition active:translate-y-2 active:shadow-none hover:bg-green-400 border-4 border-green-700 z-[1000] hover:scale-105"
                    >
                        GUESS LOCATION
                    </button>
                  )}

                   <button
                    onClick={() => setIsGuessing(false)}
                    className="absolute top-4 left-4 z-[1000] rounded-full bg-red-500 p-3 text-white shadow-lg transition hover:bg-red-600 hover:scale-110"
                    title="Back to Card"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={3} stroke="currentColor" className="w-8 h-8">
                      <path strokeLinecap="round" strokeLinejoin="round" d="M10.5 19.5 3 12m0 0 7.5-7.5M3 12h18" />
                    </svg>
                  </button>
               </div>
             </div>
           ) : (
            <div className="flex flex-col items-center gap-6 animate-in fade-in zoom-in duration-500 max-w-4xl w-full">
                <Card
                name={gameData.animal_name}
                imageUrl={gameData.image_url}
                facts={gameData.fact}
                onBack={() => setGameData(null)}
                onGuess={() => setIsGuessing(true)}
                />
            </div>
           )
        ) : (
          <>
            <h1 className="text-7xl tracking-wider text-yellow-400 drop-shadow-lg stroke-black text-center">
              BIO-GEO-GUESSER
            </h1>

            <button
              onClick={handleStartGame}
              disabled={loading}
              className="rounded-full bg-green-500 px-12 py-6 text-4xl shadow-[0_8px_0_rgb(21,128,61)] transition active:translate-y-2 active:shadow-none hover:bg-green-400 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? "LOADING..." : "START GAME"}
            </button>


          </>
        )}
      </div>
    </main>
  );
}
