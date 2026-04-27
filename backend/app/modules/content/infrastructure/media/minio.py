from __future__ import annotations

from datetime import timedelta
from typing import Any

import aioboto3  # type: ignore[import-untyped]
from botocore.config import Config  # type: ignore[import-untyped]

from app.modules.content.domain.value_objects import MediaRef


class MinioMediaStorage:
    def __init__(
        self,
        *,
        bucket: str,
        region: str,
        endpoint_url: str | None,
        access_key: str,
        secret_key: str,
        signed_url_ttl_seconds: int = 3600,
    ) -> None:
        self._bucket = bucket
        self._region = region
        self._endpoint_url = endpoint_url
        self._access_key = access_key
        self._secret = secret_key
        self._ttl = signed_url_ttl_seconds
        self._session = aioboto3.Session(
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region,
        )

    def _client_ctx(self) -> Any:
        cfg = Config(request_checksum_calculation="when_required")
        return self._session.client(
            "s3", endpoint_url=self._endpoint_url, config=cfg
        )

    async def put(self, key: str, content: bytes, mime_type: str) -> MediaRef:
        async with self._client_ctx() as s3:
            await s3.put_object(
                Bucket=self._bucket, Key=key, Body=content, ContentType=mime_type
            )
        return MediaRef(storage_key=key, mime_type=mime_type, duration_seconds=None)

    async def url_for(
        self, key: str, expires_in: timedelta = timedelta(hours=1)
    ) -> str:
        ttl = int(expires_in.total_seconds()) or self._ttl
        async with self._client_ctx() as s3:
            url: str = await s3.generate_presigned_url(
                "get_object",
                Params={"Bucket": self._bucket, "Key": key},
                ExpiresIn=ttl,
            )
            return url

    async def delete(self, key: str) -> None:
        async with self._client_ctx() as s3:
            await s3.delete_object(Bucket=self._bucket, Key=key)
