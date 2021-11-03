import fastapi

import owan.views.api


def add_routes(app: fastapi.FastAPI) -> None:
    app.add_api_route(
        "/health",
        owan.views.api.health,
        methods=["GET"],
    )

    app.add_api_route(
        "/predict",
        owan.views.api.predict,
        methods=["POST"],
    )
