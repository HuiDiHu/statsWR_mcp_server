# main.py
import contextlib
from fastapi import FastAPI
from mcp_src import statsWR_mcp_server
from mangum import Mangum

_session_started = False
_session_context = None

@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    global _session_started, _session_context
    
    if not _session_started:
        # Start session manager only once per container
        _session_context = statsWR_mcp_server.mcp.session_manager.run()
        await _session_context.__aenter__()
        _session_started = True
    
    yield

app = FastAPI(lifespan=lifespan)
app.mount("/", statsWR_mcp_server.mcp.streamable_http_app())

handler = Mangum(app)