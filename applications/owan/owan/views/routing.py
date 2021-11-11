import fastapi

import owan.views.api._converters


def add_routes(app: fastapi.FastAPI) -> None:
    app.add_api_route(
        "/health",
        owan.views.api.health,
        methods=["GET"],
        response_model=owan.views.api._converters.Health,
    )

    app.add_api_route(
        "/predict/test",
        owan.views.api.test_predict,
        methods=["POST"],
        response_model=owan.views.api._converters.PredictionRequestResponse,
    )

    app.add_api_route(
        "/predict",
        owan.views.api.predict,
        methods=["POST"],
    )
