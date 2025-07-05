# main.py
import contextlib
from fastapi import FastAPI
from mcp_src import statsWR_mcp_server
from mangum import Mangum

# combined lifespan to manage both session managers
@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    async with contextlib.AsyncExitStack() as stack:
        await stack.enter_async_context(statsWR_mcp_server.mcp.session_manager.run())
        yield


app = FastAPI(lifespan=lifespan)
app.mount("/", statsWR_mcp_server.mcp.streamable_http_app())

handler = Mangum(app)