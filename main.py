from fastapi import FastAPI
from controllers.user_controller import router as user_router
from controllers.file_controller import router as file_router
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.utils import get_openapi

# Initialize FastAPI app
app = FastAPI()

# Include the user router
app.include_router(user_router)

# Include the file router
app.include_router(file_router)

# Serve static files from the 'public' folder on the root path
app.mount("/", StaticFiles(directory="public", html=True), name="root-static")


def customize_openapi():
    if not app.openapi_schema:
        app.openapi_schema = get_openapi(
            title="ShareIt API",
            version="1.0.0",
            description="API documentation for ShareIt application",
            routes=app.routes,
        )
        # Add security components to the OpenAPI schema
        app.openapi_schema["components"] = app.openapi_schema.get("components", {})
        app.openapi_schema["components"].update(
            {
                "securitySchemes": {
                    "BasicAuth": {
                        "type": "http",
                        "scheme": "basic",
                    },
                }
            }
        )
        app.openapi_schema["security"] = [{"BasicAuth": []}]


customize_openapi()


# Custom OpenAPI schema
@app.get("/openapi.json", include_in_schema=False)
def custom_openapi():
    return app.openapi_schema


# Serve Swagger UI with updated OpenAPI schema
@app.get("/docs", include_in_schema=False)
def custom_swagger_ui_html():
    return app.openapi_schema
