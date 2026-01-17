import snowflake.connector
import os
from models.schemas import Animal,location
import json
class SnowflakeService:
    def __init__(self, connection=None):
        self.connection = connection

    def get_connection(self):
        """
        Establishes a connection to Snowflake using environment variables if one doesn't exist.
        """
        if self.connection:
            return self.connection
            
        try:
            conn = snowflake.connector.connect(
                user=os.getenv("SNOWFLAKE_USER"),
                password=os.getenv("SNOWFLAKE_PASSWORD"),
                account=os.getenv("SNOWFLAKE_ACCOUNT"),
                warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
                database=os.getenv("SNOWFLAKE_DATABASE"),
                schema=os.getenv("SNOWFLAKE_SCHEMA")
            )
            return conn
        except Exception as e:
            print(f"Error connecting to Snowflake: {e}")
            raise e






    def execute_query(self, query, params=None):
        """
        Executes a general SQL query.
        
        Args:
            query (str): The SQL query to execute.
            params (tuple, optional): Parameters to bind to the query.
            
        Returns:
            The result of the query.
        """
        # If we have a persistent connection, use it. Otherwise, create a temporary one.
        conn = self.get_connection() if self.connection else self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(query, params)
            result = cursor.fetchall()
            return result
        except Exception as e:
            print(f"Error executing query: {e}")
            raise e
        finally:
            cursor.close()
            # Only close the connection if it's NOT a persistent one we are managing
            if not self.connection:
                 conn.close()







    def get_animals_id(self):
        query = "SELECT species_key FROM biogeoguesser.public.golden_animal"
        res = self.execute_query(query)
        species_list = [row[0] for row in res]
        return species_list





    def get_animal_by_id(self,id):
        query = "call get_species_data(%s)"
        res = self.execute_query(query, (id,))
        animal_name = res[0][1]
        species_key = res[0][0]
        image_url = res[0][2]
        fact = res[0][3]
        return Animal(animal_name,species_key,image_url,fact)


    def get_location(self, id):
        query = "call get_animal_locations(%s)"
        res = self.execute_query(query, (id,))
        
        if not res:
            return None  # Or handle empty results as needed

        species_key = id
        
        # 1. Parse 'locations' string into a list and force floats to remove scientific notation
        raw_locations = json.loads(res[0][2]) if isinstance(res[0][2], str) else res[0][2]
        cleaned_locations = [
            {"lat": float(item['lat']), "lon": float(item['lon'])} 
            for item in raw_locations
        ]

        # 2. Parse 'geo_hashes' (usually just a list of strings)
        cleaned_geohashes = json.loads(res[0][3]) if isinstance(res[0][3], str) else res[0][3]

        # 3. Return the formatted data
        return location(species_key, cleaned_locations, cleaned_geohashes)