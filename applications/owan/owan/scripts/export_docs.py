"""
Export docs as staric HTML file.
For detail, please check: https://github.com/Redocly/redoc/issues/726.
"""
import json
import pathlib
import sys

if sys.version_info >= (3, 8):
    from typing import Final
else:
    from typing_extensions import Final

import owan.wsgi

HTML_TEMPLATE: Final = """<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="content-type" content="text/html; charset=UTF-8">
    <title>My Project - ReDoc</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="shortcut icon" href="https://fastapi.tiangolo.com/img/favicon.png">
    <style>
        body {
            margin: 0;
            padding: 0;
        }
    </style>
    <style data-styled="" data-styled-version="4.4.1"></style>
</head>
<body>
    <div id="redoc-container"></div>
    <script src="https://cdn.jsdelivr.net/npm/redoc/bundles/redoc.standalone.js"> </script>
    <script>
        var spec = %s;
        Redoc.init(spec, {}, document.getElementById("redoc-container"));
    </script>
</body>
</html>
"""

if __name__ == "__main__":
    output_path: Final = pathlib.Path("./tmp/api.html")
    app: Final = owan.wsgi.main()

    with output_path.open(mode="w") as f:
        print(HTML_TEMPLATE % json.dumps(app.openapi()), file=f)
