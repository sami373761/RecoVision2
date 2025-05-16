FROM python:3.9.7-slim

ENV PYTHONBUFFERED=1
ENV PORT=8000
ENV DJANGO_SETTINGS_MODULE=movieWeb.settings

WORKDIR /app

COPY . /app/

# Gerekli bağımlılıkları yükle
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    python3-dev \
    libffi-dev \
    libjpeg-dev \
    zlib1g-dev \
    libpq-dev \
    libmariadb-dev \
    liblapack-dev \
    libopenblas-dev \
    gfortran \
    bash \
    libxml2-dev \
    libxslt-dev \
    make \
    git && \
    rm -rf /var/lib/apt/lists/*

# Pip'i güncelle
RUN pip install --upgrade pip

# PyTorch ve Tensorflow'u manuel yükle (çünkü Alpine uyumsuz!)
RUN pip install torch==2.2.2 --extra-index-url https://download.pytorch.org/whl/cpu

# Bağımlılıkları yükle
RUN pip install --no-cache-dir -r requirements.txt

# Statik dosyaları topla
RUN python3 manage.py collectstatic --noinput

# NLTK veri setlerini indir
RUN python -c "import nltk; nltk.download('punkt_tab'); nltk.download('stopwords'); nltk.download('wordnet')"

CMD gunicorn movieWeb.wsgi:application --bind 0.0.0.0:"${PORT}" --timeout 300
EXPOSE ${PORT}
