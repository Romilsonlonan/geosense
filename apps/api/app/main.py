from contextlib import asynccontextmanager
from dataclasses import asdict, dataclass

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


@dataclass(frozen=True, slots=True)
class ServiceStatus:
    name: str
    status: str


@asynccontextmanager
async def lifespan(_: FastAPI):
    yield


app = FastAPI(title="GeoSense API", version="0.1.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/health", response_model=ServiceStatus)
def health() -> ServiceStatus:
    """Readiness endpoint; HTTP spans are added by OpenTelemetry middleware."""
    return ServiceStatus(name="geosense-api", status="ok")


@app.get("/api/v1/status")
def status() -> dict[str, object]:
    return {"service": asdict(health()), "domains": ["climate", "seismology", "soil", "vegetation", "hydrology", "oceanography"]}
