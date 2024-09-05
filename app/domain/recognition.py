import time

import jwt
from aiohttp import ClientSession
import json

from pydantic import TypeAdapter

from app import dto


class YandexSpeechKit:
    def __init__(self):
        self.transcribe_url = "https://transcribe.api.cloud.yandex.net/speech/stt/v2/longRunningRecognize"
        self.operation_url = "https://operation.api.cloud.yandex.net/operations/{operation_id}"
        self.session = ClientSession()
        self.authorized_session = None

    async def create_authorized_session(self):
        with open('authorized_key.json.txt', 'r') as f:
            obj = f.read()
            obj = json.loads(obj)
            private_key = obj['private_key']
            key_id = obj['id']
            service_account_id = obj['service_account_id']

        now = int(time.time())
        payload = {
            'aud': 'https://iam.api.cloud.yandex.net/iam/v1/tokens',
            'iss': service_account_id,
            'iat': now,
            'exp': now + 3600
        }

        encoded_token = jwt.encode(
            payload,
            private_key,
            algorithm='PS256',
            headers={'kid': key_id}
        )
        body = {"jwt": encoded_token}
        async with self.session.post(url="https://iam.api.cloud.yandex.net/iam/v1/tokens", data=json.dumps(body)) as resp:
            data = await resp.json()
            self.authorized_session = ClientSession(
                headers={
                    "Authorization": f"Bearer {data.get('iamToken')}",
                    "Content-Type": "application/json",
                }
            )

    async def recognize(self, audio_uri: str):
        await self.create_authorized_session()
        body = {
            "config": {
                "specification": {
                    "languageCode": "ru-RU",
                    "profanityFilter": False,
                    "literature_text": True,
                    "audioEncoding": "LINEAR16_PCM",
                    "sampleRateHertz": 16000,
                    "audioChannelCount": 1,
                    "rawResults": False,
                    "model": "general:rc",
                    "audioProcessingType": "FULL_DATA",
                    "languageRestriction": {
                        "restrictionType": "WHITELIST",
                        "languageCode": [
                            "ru-RU"
                        ]
                    }
                }
            },
            "audio": {
                "uri": audio_uri
            }
        }
        async with self.authorized_session.post(url=self.transcribe_url, data=json.dumps(body)) as response:
            try:
                data = await response.json()
                adapter = TypeAdapter(dto.SpeechKit)
                return adapter.validate_python(data)
            except Exception as e:
                return e

    async def get_operation(self, operation_id: str):
        await self.create_authorized_session()
        async with self.authorized_session.get(url=self.operation_url.format(operation_id=operation_id)) as response:
            try:
                data = await response.json()
                print(data)
                adapter = TypeAdapter(dto.SpeechKit)
                validated_data = adapter.validate_python(data)
                return validated_data
            except Exception as e:
                return e


    async def close(self):
        await self.session.close()
        await self.authorized_session.close()
