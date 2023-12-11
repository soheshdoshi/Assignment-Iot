from fastapi import APIRouter, Request

router = APIRouter()


@router.get("/")
def check_endpoint(request: Request):
    """
    this method will use to check health.
    """
    return {"status ": "running"}

