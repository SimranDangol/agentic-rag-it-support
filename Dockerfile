FROM python:3.11-slim

# Set up user for Hugging Face Spaces (UID 1000) and directories
RUN useradd -m -u 1000 user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH \
    HF_HOME=/home/user/.cache/huggingface

WORKDIR /app

# Install CPU-only torch first to avoid downloading the CUDA version
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Pre-download sentence-transformer models into shared cache so container is self-contained
RUN python -c "\
from sentence_transformers import SentenceTransformer, CrossEncoder; \
SentenceTransformer('all-MiniLM-L6-v2'); \
CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')"

WORKDIR $HOME/app
COPY --chown=user:user . $HOME/app

USER user

EXPOSE 7860

CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "7860"]
