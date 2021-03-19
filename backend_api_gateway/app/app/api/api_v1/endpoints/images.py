from typing import Any
import uuid
from uuid import UUID
from fastapi import (
    APIRouter,
    Response,
    Path,
)
from fastapi.param_functions import Depends

from app.schemas.images import ImageUploadResponse, ImagesUrlsResponse, ImagesExpiredDateDownload
from app.api.deps import SenderImages, ReceiveImages

router = APIRouter()


@router.post("/", response_model=ImageUploadResponse)
async def upload_images(
    # images: List[UploadFile] = File(...),
    response: Response,
    images: SenderImages = Depends(SenderImages),
) -> Any:
    response_upload = images.response_upload
    response.status_code = response_upload[0]
    image_upload_response = ImageUploadResponse(
        **response_upload[1],
        # uuid=uuid.uuid4()
    )
    return image_upload_response


@router.get("/{uuid}")
async def download_images(
    response: Response,
    uuid: UUID = Path(..., title="The UUID of the workspace to consult the images."),
    receiver:  ReceiveImages = Depends(ReceiveImages)
) -> Any:
    response_download = receiver.download_images(uuid=uuid)
    if not response_download[1]['expired']:
        images = ImagesUrlsResponse(
            **response_download[1]
        )
    else:
        images = ImagesExpiredDateDownload(
            **response_download[1]
        )
    response.status_code = response_download[0]
    return images
