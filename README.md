# Bio-Geo-Guesser

Bio-Geo-Guesser is a web application backend that combines biological data with geolocation features. It leverages [FastAPI](https://fastapi.tiangolo.com/) for a high-performance REST API and [Snowflake](https://www.snowflake.com/) for robust data storage and retrieval.

## Features

- **FastAPI Backend**: Efficient and modern Python web framework.
- **Snowflake Integration**: Secure and scalable data warehousing.
- **Geohash Support**: Geospatial data handling.
- **Data Caching**: In-memory caching for optimized read performance.

## Project Structure

```
bio-geo-guesser/
├── backend/
│   ├── core/
│   ├── models/
│   ├── scoring/
│   ├── services/
│   │   └── snowflake.py    # Snowflake interaction logic
│   └── main.py             # Application entry point
├── database/
│   ├── database-script/
│   └── snowflake/
├── .env                    # Environment variables (not committed)
├── requirements.txt        # Python dependencies
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.8+
- A Snowflake account with appropriate credentials.

### Installation

1. Clone the repository:

   ```bash
   git clone <repository_url>
   cd bio-geo-guesser
   ```

2. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # macOS/Linux
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Configuration

Create a `.env` file in the root directory and add your Snowflake credentials and application settings:

```ini
SNOWFLAKE_USER=your_user
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_ACCOUNT=your_account_identifier
SNOWFLAKE_WAREHOUSE=your_warehouse
SNOWFLAKE_DATABASE=your_database
SNOWFLAKE_SCHEMA=your_schema

# Optional
PORT=8000
IP=127.0.0.1
```

## Usage

### Running the Server

Start the application using the included runner in `main.py`:

```bash
python backend/main.py
```

Or run with `uvicorn` directly:

```bash
uvicorn backend.main:app --reload
```

The server will start at `http://127.0.0.1:8000`.

### API Endpoints

- `GET /`: Returns a list of available animal IDs.
- `GET /animal/{id}`: Retrieve details for a specific animal.
- `GET /location/{id}`: Retrieve location data for a specific animal.

You can also access the auto-generated API documentation at:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`
