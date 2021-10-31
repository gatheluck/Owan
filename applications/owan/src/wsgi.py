import sys
import fastapi
if sys.version_info >= (3, 8):
    from typing import Final
else:
    from typing_extensions import Final

import src.views.routing


def main() -> fastapi.FastAPI:
    app: Final = fastapi.FastAPI()
    src.views.routing.add_routes(app)

    return app