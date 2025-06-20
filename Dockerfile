FROM ghcr.io/docling-project/docling-serve-cu124:latest

# Install Cog
RUN pip install cog

# Copy Cog interface
COPY predict.py /src/predict.py
COPY cog.yaml /src/cog.yaml

WORKDIR /src

# Environment for CUDA and docling-serve (can be extended as needed)
ENV DOCLING_SERVE_PORT=5001 \
    DOCLING_SERVE_MAX_SYNC_WAIT=600 \
    DOCLING_SERVE_ENG_KIND=local \
    DOCLING_SERVE_ENG_LOC_NUM_WORKERS=2 \
    CUDA_VISIBLE_DEVICES=0 