"use client";

import { Luckiest_Guy } from "next/font/google";

const luckiestGuy = Luckiest_Guy({
  weight: "400",
  subsets: ["latin"],
});

export default function Card({ name, imageUrl, facts, onBack, onGuess }) {
  return (
    <div
      className={`relative mx-auto flex max-w-4xl flex-col overflow-hidden rounded-xl bg-white shadow-2xl ring-4 ring-yellow-400 md:flex-row ${luckiestGuy.className}`}
    >
      <button
        onClick={onBack}
        className="absolute left-2 top-2 z-10 rounded-full bg-red-500 p-2 text-white shadow-lg transition hover:bg-red-600 hover:scale-110"
        title="Back to Home"
      >
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2.5} stroke="currentColor" className="w-6 h-6">
          <path strokeLinecap="round" strokeLinejoin="round" d="m2.25 12 8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25" />
        </svg>
      </button>

      <div className="bg-gray-200 md:w-1/2">
        {imageUrl ? (
          <img
            src={imageUrl}
            alt={name}
            className="h-full w-full object-contain bg-black"
          />
        ) : (
          <div className="flex h-64 items-center justify-center text-gray-400 md:h-full">
            No Image
          </div>
        )}
      </div>

      <div className="flex flex-col p-6 md:w-1/2 bg-blue-50">
        <div className="bg-blue-600 p-3 text-center rounded-lg mb-6 shadow-md border-2 border-blue-800">
          <h2 className="text-3xl uppercase tracking-wider text-yellow-300 drop-shadow-md stroke-black">
            {name}
          </h2>
        </div>

        <div className="flex flex-1 flex-col gap-6">
            <div className="flex-1 rounded-lg border-2 border-blue-200 bg-white p-4 overflow-y-auto max-h-60">
                <h3 className="text-xl text-blue-800 underline decoration-yellow-400 decoration-4 mb-2">
                Fun Facts:
                </h3>
                <p className="text-lg leading-relaxed text-blue-900">
                {facts || "No facts available for this amazing creature yet!"}
                </p>
            </div>

            <div className="flex justify-center">
                 <button 
                    onClick={onGuess}
                    className="rounded-full bg-green-500 px-8 py-2 text-xl font-bold text-white shadow-[0_4px_0_rgb(21,128,61)] transition active:translate-y-1 active:shadow-none hover:bg-green-400 border-2 border-green-700"
                 >
                    GUESS
                 </button>
            </div>
        </div>
      </div>
    </div>
  );
}
