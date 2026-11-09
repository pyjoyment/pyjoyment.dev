FROM python:3.15-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:0.11.19 /uv /bin/
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_NO_DEV=1 UV_PYTHON_DOWNLOADS=0
WORKDIR /opt/app
ENV VIRTUAL_ENV=/opt/app/.venv
COPY app.py ./
RUN uv venv && uv sync --script app.py --active

FROM python:3.15-slim
WORKDIR /opt/app
COPY --from=builder /opt/app/.venv .venv
COPY . .
ENV PATH="/opt/app/.venv/bin:$PATH"
ARG PORT=3000
ENV PORT=${PORT}
EXPOSE ${PORT}
HEALTHCHECK --timeout=3s --start-period=30s --start-interval=1s CMD ["python", "-c", "import http.client, os, sys; c = http.client.HTTPConnection('127.0.0.1', int(os.environ['PORT']), timeout=2); c.request('GET', '/livez'); sys.exit(c.getresponse().status != 200)"]
CMD ["python", "app.py", "prefork"]
