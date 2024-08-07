from starlette.routing import BaseRoute, Mount, Route
from starlette.requests import Request
from starlette.responses import JSONResponse


async def health_check(request: Request):
    print(request.query_params.getlist("platform"))
    return JSONResponse(
        {
            "status": 200,
        }
    )


api_routes = [Route("/", health_check, methods=["GET"])]
