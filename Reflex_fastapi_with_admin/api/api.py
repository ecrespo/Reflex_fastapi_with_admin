from fastapi.responses import HTMLResponse

async def hello():
    return {"message": "Hello, World!"}


async def get_admin() -> HTMLResponse:
    return HTMLResponse('<a href="/admin/">Click me to get to Admin!</a>')

