import os

import aiobotocore.endpoint
import pytest
from aiobotocore.endpoint import StreamingBody
from moto import mock_aws

from app.modules.content.infrastructure.media.minio import MinioMediaStorage

# aiobotocore 2.x does `await http_response.content` but moto's stubber returns
# a plain-bytes AWSResponse (not a coroutine). Replace convert_to_response_dict
# with a version that handles both cases.

try:
    import httpx  # type: ignore[import-untyped]
except ImportError:
    httpx = None  # type: ignore[assignment]


async def _moto_compat_convert(http_response, operation_model):  # type: ignore[no-untyped-def]
    async def _get_content():  # type: ignore[no-untyped-def]
        val = http_response.content
        if isinstance(val, bytes):
            return val
        return await val

    response_dict = {
        "headers": http_response.headers,
        "status_code": http_response.status_code,
        "context": {"operation_name": operation_model.name},
    }
    if response_dict["status_code"] >= 300:
        response_dict["body"] = await _get_content()
    elif operation_model.has_event_stream_output:
        response_dict["body"] = http_response.raw
    elif operation_model.has_streaming_output:
        if httpx and isinstance(http_response.raw, httpx.Response):
            from aiobotocore.endpoint import HttpxStreamingBody

            response_dict["body"] = HttpxStreamingBody(http_response.raw)
        else:
            length = response_dict["headers"].get("content-length")
            response_dict["body"] = StreamingBody(http_response.raw, length)
    else:
        response_dict["body"] = await _get_content()
    return response_dict


@pytest.fixture(autouse=True)
def patch_aiobotocore_convert(monkeypatch):
    monkeypatch.setattr(aiobotocore.endpoint, "convert_to_response_dict", _moto_compat_convert)


@pytest.fixture
def minio_storage():
    with mock_aws():
        os.environ.setdefault("AWS_DEFAULT_REGION", "us-east-1")
        os.environ.setdefault("AWS_ACCESS_KEY_ID", "test")
        os.environ.setdefault("AWS_SECRET_ACCESS_KEY", "test")

        import boto3

        client = boto3.client("s3", region_name="us-east-1")
        client.create_bucket(Bucket="test-bucket")
        yield MinioMediaStorage(
            bucket="test-bucket",
            region="us-east-1",
            endpoint_url=None,
            access_key="test",
            secret_key="test",
            signed_url_ttl_seconds=60,
        )


@pytest.mark.asyncio
async def test_put_uploads_and_url_is_signed(minio_storage):
    ref = await minio_storage.put("pieces/x/audio.mp3", b"abc", "audio/mpeg")
    assert ref.storage_key == "pieces/x/audio.mp3"
    url = await minio_storage.url_for("pieces/x/audio.mp3")
    assert "pieces/x/audio.mp3" in url
    assert "Signature=" in url or "X-Amz-Signature" in url


@pytest.mark.asyncio
async def test_delete_round_trip(minio_storage):
    await minio_storage.put("k.mp3", b"x", "audio/mpeg")
    await minio_storage.delete("k.mp3")
