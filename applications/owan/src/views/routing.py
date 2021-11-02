import fastapi

import src.views.api


def add_routes(app: fastapi.FastAPI) -> None:
    app.add_api_route(
        "/health",
        src.views.api.health,
        methods=["GET"],
    )
