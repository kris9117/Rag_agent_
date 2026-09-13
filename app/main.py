import logging

from fastapi import FastAPI

from app.config import get_settings
from app.services.logging_config import setup_logging
from app.api.routes import router as support_router


settings = get_settings()

setup_logging(settings.log_level)

logger = logging.getLogger(__name__)


app = FastAPI(
    title="Enterprise IT Support & Resolution Agent",
    version="0.1.0",
    description="Enterprise-style GenAI IT support agent.",
)

app.include_router(support_router)

logger.info(
    "Application started | environment=%s",
    settings.app_env,
)





@app.get("/health")
def health_check() -> dict[str, str]:
    logger.info("Health check requested")

    return {
        "status": "healthy",
        "service": "enterprise-it-support-agent",
    }