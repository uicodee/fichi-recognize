import asyncio

from fastapi import APIRouter, UploadFile, HTTPException, status, Path
from sse_starlette import EventSourceResponse

from app.config import load_config
from app.domain.recognition import YandexSpeechKit
from app.domain.storage import S3StorageService

router = APIRouter(prefix="/recognize")


async def operation_checker(yandex_speech_kit: YandexSpeechKit, operation_id: str):
    while True:
        operation = await yandex_speech_kit.get_operation(operation_id=operation_id)
        if operation.done:
            text = ""
            for chunk in operation.response.chunks:
                for alternative in chunk.alternatives:
                    text += alternative.text + " "
            yield {
                "event": "message",
                "data": "[STARTSTREAM]"
            }
            yield {
                "event": "message",
                "data": text
            }
            yield {
                "event": "message",
                "data": "[DONE]"
            }
            await yandex_speech_kit.close()
            break
        else:
            yield {
                "event": "message",
                "data": "[PROCESSING]"
            }
        await asyncio.sleep(1)


@router.post(
    path="/"
)
async def recognize_audio(audio: UploadFile):
    if audio.content_type not in ["audio/wav", "audio/wave"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Audio file must be audio",
        )
    settings = load_config()
    s3 = S3StorageService(settings=settings)
    yandex_speech_kit = YandexSpeechKit()
    path = await s3.upload(file=audio)
    operation = await yandex_speech_kit.recognize(audio_uri=path)
    return EventSourceResponse(operation_checker(yandex_speech_kit, operation.id))


@router.get(path="/{operation_id}")
async def get_operation(operation_id: str = Path()):
    yandex_speech_kit = YandexSpeechKit()
    return EventSourceResponse(operation_checker(yandex_speech_kit, operation_id))


@router.on_event("shutdown")
async def shutdown_event():
    yandex_speech_kit = YandexSpeechKit()
    await yandex_speech_kit.close()
