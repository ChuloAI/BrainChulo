from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def sample_plugin_route():
    return {"message": "Sample plugin route"}

# Additional routes and functionality for the sample plugin
