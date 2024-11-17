import pytest

from aphrodite.common.utils import FlexibleArgumentParser
from aphrodite.endpoints.openai.api_server import build_async_engine_client
from aphrodite.endpoints.openai.args import make_arg_parser


@pytest.mark.asyncio
async def test_mp_crash_detection():

    with pytest.raises(RuntimeError) as excinfo:
        parser = FlexibleArgumentParser(
            description="Aphrodite's remote OpenAI server.")
        parser = make_arg_parser(parser)
        args = parser.parse_args([])
        # use an invalid tensor_parallel_size to trigger the
        # error in the server
        args.tensor_parallel_size = 65536

        async with build_async_engine_client(args):
            pass
    assert "The server process died before responding to the readiness probe"\
          in str(excinfo.value)


@pytest.mark.asyncio
async def test_mp_cuda_init():
    # it should not crash, when cuda is initialized
    # in the API server process
    import torch
    torch.cuda.init()
    parser = FlexibleArgumentParser(
        description="Aphrodite's remote OpenAI server.")
    parser = make_arg_parser(parser)
    args = parser.parse_args([])

    async with build_async_engine_client(args):
        pass