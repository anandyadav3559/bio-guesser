from services.snowflake import SnowflakeService
import os
from dotenv import load_dotenv

load_dotenv()

def db_connection():
    print("Testing Snowflake Connection...")
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
    if not os.getenv("SNOWFLAKE_USER"):
        print("Please set your Snowflake credentials in the .env file before running this test.")
    else:
        db_connection()
    service = SnowflakeService()
    ids = service.get_animals_id()
    animal = service.get_animal_by_id(5219416)
    location = service.get_location(5219416)
    print(animal.to_dict())
    print(location.to_dict())
