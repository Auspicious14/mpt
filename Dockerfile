FROM python:3.11-slim-bullseye

WORKDIR /MoneyPrinterTurbo

RUN chmod 777 /MoneyPrinterTurbo

ENV PYTHONPATH="/MoneyPrinterTurbo"

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    imagemagick \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Fix ImageMagick security policy
RUN sed -i '/<policy domain="path" rights="none" pattern="@\*"/d' /etc/ImageMagick-6/policy.xml

# Copy requirements and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Render uses PORT environment variable
ENV PORT=8080

# Expose the port
EXPOSE 8080

# Run the API server (main.py)
CMD python main.py