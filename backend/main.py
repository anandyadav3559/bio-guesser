import fastapi
from dotenv import load_dotenv
import uvicorn
import os
import random
import sys

# Ensure backend directory is in python path for imports if running from root
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from services.snowflake import SnowflakeService
from scoring.get_score import score_guess
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

load_dotenv()

ids = []
global_service = None
locations = []

@asynccontextmanager
async def lifespan(app: fastapi.FastAPI):
    global ids
    global global_service
    try:
        print("Loading cached data from Snowflake...")
        
        if not os.getenv("SNOWFLAKE_USER"):
            print("WARNING: Snowflake credentials not found in environment variables.")
        
        # Initialize the global service with a persistent connection
        temp_service = SnowflakeService()
        conn = temp_service.get_connection()
        print("Established persistent Snowflake connection.")
        
        # Store it in a global service instance
        global_service = SnowflakeService(connection=conn)

        ids = global_service.get_animals_id()
        print(f"Loaded {len(ids)} IDs.")
    except Exception as e:
        print(f"Error loading data on startup: {e}")
    yield
    print("Shutting down...")
    if global_service and global_service.connection:
        global_service.connection.close()

app = fastapi.FastAPI(lifespan=lifespan)

# CORS Configuration
# In production, set ALLOWED_ORIGINS to your Vercel URL (e.g. https://my-app.vercel.app)
# For development, defaults to localhost:3000
origins_env = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000")
origins = [origin.strip() for origin in origins_env.split(",")]

# Add wildcard for easier testing if needed (optional, safer to stick to specific domains)
# origins.append("https://*.vercel.app") 

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/get_score")
def get_score(lat: float, lng: float):
    global locations
    if not locations:
        return {"error": "Game not started or no location data"}
    
    # Transform locations object to list of tuples [(lat, lon)]
    # locations.locations is [{'lat': ..., 'lon': ...}]
    sightings = [(loc['lat'], loc['lon']) for loc in locations.locations]
    
    score = score_guess(lat, lng, sightings)
    
    # Add all sightings to the response for visualization
    score["all_sightings"] = [{"lat": lat, "lng": lon} for lat, lon in sightings]
    
    return score



@app.get("/start_game")
def start_game():
    global locations
    if not ids:
        return {"error": "No IDs available. Database might be empty or connection failed."}
    
    random_id = random.choice(ids)
    
    # Use existing logic to get animal by ID
    service = global_service if global_service else SnowflakeService()
    animal = service.get_animal_by_id(random_id)
    locations = service.get_location(random_id)
    return animal.to_dict()


@app.get("/animal/{id}")
def get_animal_by_id(id: int):
    service = global_service if global_service else SnowflakeService()
    animal = service.get_animal_by_id(id)
    return animal.to_dict()

@app.get("/location/{id}")
def get_location(id: int):
    # This seems to have a bug in original code: 'location' was not defined.
    # Assuming intent:
    service = global_service if global_service else SnowflakeService()
    loc = service.get_location(id)
    return loc.to_dict()

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Backend is running"}

if __name__ == "__main__":
    port = int(os.getenv('PORT', 8000))
    # Listen on 0.0.0.0 to ensure external availability if running directly
    uvicorn.run(app, host="0.0.0.0", port=port)
