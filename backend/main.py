import fastapi
from dotenv import load_dotenv
import snowflake.connector
import uvicorn
import os
import random
from services.snowflake import SnowflakeService
from scoring.get_score import score_guess
load_dotenv()
from fastapi.middleware.cors import CORSMiddleware

from contextlib import asynccontextmanager

ids = []
global_service = None
locations = []
@asynccontextmanager
async def lifespan(app: fastapi.FastAPI):
    global ids
    global global_service
    try:
        print("Loading cached data from Snowflake...")
        
        # Initialize the global service with a persistent connection
        # We create a temporary service just to use its logic to get a connection, 
        # or we could just use the connector directly. 
        # Let's use a cleaner way: establish connection and pass it.
        
        if not os.getenv("SNOWFLAKE_USER"):
            print("Please set your Snowflake credentials in the .env file.")
            return

        # Create the initial connection
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js dev URL
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
        return {"error": "No IDs available"}
    
    random_id = random.choice(ids)
    
    # Use existing logic to get animal by ID
    service = global_service if global_service else SnowflakeService()
    animal = service.get_animal_by_id(random_id)
    locations = service.get_location(random_id)
    return animal.to_dict()


@app.get("/animal/{id}")
def get_animal_by_id(id: int):
    # Use the global service if available, else fallback (though lifespan should have set it)
    service = global_service if global_service else SnowflakeService()
    animal = service.get_animal_by_id(id)
    return animal.to_dict()

@app.get("/location/{id}")
def get_location(id: int):
    service = global_service if global_service else SnowflakeService()
    return location.to_dict()

def db_connection():
    print("Testing Snowflake Connection...")
    # This function is now legacy/unused in the main flow but good for debugging
    service = SnowflakeService()
    try:
        conn = service.get_connection()
        print("Successfully connected to Snowflake!")
        
        cursor = conn.cursor()
        cursor.execute("SELECT CURRENT_VERSION()")
        version = cursor.fetchone()
        print(f"Snowflake Version: {version[0]}")
        
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Failed to connect: {e}")





if __name__ == "__main__":
    # Optional: Run a quick connection test before starting server
        
    port = int(os.getenv('PORT', 8000))
    ip = os.getenv('IP', '127.0.0.1') # Defaulting to localhost if not set
    
    # Run uvicorn
    # Note: When running programmatically like this, lifespan events *should* fire.
    uvicorn.run(app, host=ip, port=port)