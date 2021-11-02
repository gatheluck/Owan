from fastapi.responses import JSONResponse


async def health() -> JSONResponse:
    return JSONResponse({"health": "ok"})
