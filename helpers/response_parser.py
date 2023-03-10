from fastapi.responses import JSONResponse


def response(message: str, code=None, data=None, access_token: str | None = None):
    if code in [200, 201, 202, 203]:
        if access_token:
            return JSONResponse(status_code=code, content={"access_token": access_token, "status": "success"})
        return JSONResponse(status_code=code, content={"message": message, "data": data, "status": "success"})
    return JSONResponse(status_code=code, content={"message": message, "data": data, "status": "error"})
