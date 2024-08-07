import uvicorn
from starlette.routing import Mount
from starlette.applications import Starlette

from .api_routes import api_routes


app = Starlette(debug=True, routes=[Mount("/api", routes=api_routes)])


if __name__ == "__main__":
    uvicorn.run("src.server.app:app", host="localhost", port=8000, reload=True)
