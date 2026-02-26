import logging
import json
from uuid import uuid4
from starlette.requests import Request
from starlette.middleware.base import BaseHTTPMiddleware
from contextvars import ContextVar

# ContextVar to store the current request ID
request_id_ctx = ContextVar("request_id", default=None)

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "message": record.getMessage(),
            "loggerName": record.name,
            "filename": record.filename,
            "lineno": record.lineno,
        }
        # Add extra attributes from the log record
        if hasattr(record, 'extra_fields'):
            log_record.update(record.extra_fields)

        # Add request_id if present
        request_id = request_id_ctx.get()
        if request_id:
            log_record["request_id"] = request_id

        if record.exc_info:
            log_record["exc_info"] = self.formatException(record.exc_info)
        
        if record.stack_info:
            log_record["stack_info"] = self.formatStack(record.stack_info)

        return json.dumps(log_record)

def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Remove existing handlers to avoid duplicate logs
    if logger.handlers:
        for handler in logger.handlers:
            logger.removeHandler(handler)

    handler = logging.StreamHandler()
    formatter = JsonFormatter()
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # Configure uvicorn loggers to use our formatter
    for logger_name in ['uvicorn', 'uvicorn.access', 'uvicorn.error']:
        uvicorn_logger = logging.getLogger(logger_name)
        uvicorn_logger.setLevel(logging.INFO)
        if uvicorn_logger.handlers:
            for handler in uvicorn_logger.handlers:
                uvicorn_logger.removeHandler(handler)
        uvicorn_logger.addHandler(handler)

class CorrelationIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Generate a new request ID or get from header
        request_id = request.headers.get("X-Request-ID") or request.headers.get("dapr-traceid") or str(uuid4())
        
        # Store the request ID in the context variable
        token = request_id_ctx.set(request_id)
        
        response = await call_next(request)
        
        # Add request ID to response headers
        response.headers["X-Request-ID"] = request_id
        
        # Reset the context variable
        request_id_ctx.reset(token)
        
        return response
