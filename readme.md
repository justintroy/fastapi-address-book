## Setup

### Clone the Repository

```bash
git clone https://github.com/justintroy/fastapi-address-book.git
cd fastapi-address-book
```

### Create a virtual environment
```bash
python -m venv venv
```

### Activate the virtual environment (Linux/Mac)
```bash
source venv/bin/activate
```

### Activate the virtual environment (Windows)
```
.\venv\Scripts\activate
```

### Install dependencies
```bash
pip install -r requirements.txt
```

### Setup database tables with Alembic
```bash
alembic init -t async alembic
alembic revision --autogenerate -m "Initial tables"
alembic upgrade head

```

### Start the app
```bash
uvicorn src.main:app --reload --port 5080
```

### Open the app in the browser
http://localhost:5080

### Explore the docs
http://localhost:5080/docs


