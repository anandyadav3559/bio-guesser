Live-Link : https://bio-guesser.vercel.app/
Bio-Geo-Guesser is a web application that combines biological data with geolocation features to create an interactive guessing game. It leverages a robust architecture with a **FastAPI** backend for high-performance data serving, a **Next.js** frontend for a dynamic user experience, and **Snowflake** for scalable data storage.


https://github.com/user-attachments/assets/ed58239d-e2cd-40cd-a27b-26d2d7b80deb

## Features


- **Interactive Frontend**: Built with Next.js and TailwindCSS for a responsive and modern UI.
- **Geospatial Visualization**: Integrated Leaflet maps to visualize animal locations.
- **FastAPI Backend**: Efficient REST API for serving biological data and game logic.
- **Snowflake Integration**: Secure and scalable warehousing for large datasets.
- **Automated Data Pipeline**: Python scripts to fetch and ingest biological data from GBIF API.
- **Geohash Support**: Efficient geospatial querying and clustering.

## Tech Stack
<img width="1536" height="1024" alt="bio-geo-guesser-architecture" src="https://github.com/user-attachments/assets/7ae16584-38d4-4bfc-bb12-5339720836f3" />

### Frontend

- **Framework**: [Next.js](https://nextjs.org/) (React)
- **Styling**: [TailwindCSS](https://tailwindcss.com/)
- **Maps**: [Leaflet](https://leafletjs.com/) & React-Leaflet

### Backend

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **Database Connector**: Snowflake Connector for Python
- **Utilities**: Python-Geohash, Dotenv

### Data Pipeline

- **Source**: [GBIF API](https://www.gbif.org/developer/summary)
- **Ingestion**: Python scripts with Airflow support (in progress)

## Project Structure

```
bio-geo-guesser/
├── backend/
│   ├── core/
│   ├── models/
│   ├── scoring/
│   ├── services/
│   │   └── snowflake.py    # Snowflake database interactions
│   └── main.py             # FastAPI entry point
├── front-end/
│   └── bio-geoguesser-frontend/
│       ├── src/
│       ├── public/
│       └── package.json    # Frontend dependencies
├── database/
│   ├── database-script/
│   │   ├── api.py          # Data fetching script
│   │   └── upload.sh       # Upload trigger script
│   └── snowflake/
├── .env                    # Backend environment variables
├── requirements.txt        # Backend dependencies
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.8+
- Node.js 18+ and npm
- A Snowflake account with appropriate credentials.

### Installation

#### 1. Clone the Repository

```bash
git clone <repository_url>
cd bio-geo-guesser
```

#### 2. Backend Setup

Create a virtual environment and install dependencies:

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
```

#### 3. Frontend Setup

Navigate to the frontend directory and install dependencies:

```bash
cd front-end/bio-geoguesser-frontend
npm install
```

#### 4. Data Ingestion (Optional)

To populate your database with initial data:

```bash
cd ../../database/database-script
# Run the fetching script (fetches King Cobra data by default)
python api.py
```

### Configuration

#### Backend Configuration

Create a `.env` file in the root directory:

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

#### Frontend Configuration

Create a `.env.local` file in `front-end/bio-geoguesser-frontend/` if needed for custom API endpoints:

```ini
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Usage

### Running the Backend

From the root directory:

```bash
python backend/main.py
# OR
uvicorn backend.main:app --reload
```

Server running at `http://127.0.0.1:8000`

### Running the Frontend

From `front-end/bio-geoguesser-frontend`:

```bash
npm run dev
```

Frontend running at `http://localhost:3000`



### API Endpoints Overview

- `GET /`: List animal IDs.
- `GET /animal/{id}`: Get animal details.
- `GET /location/{id}`: Get animal location data.
