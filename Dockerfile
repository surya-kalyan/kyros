FROM python:3.11-slim

RUN apt-get update && apt-get install -y ffmpeg nginx && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN mkdir -p uploads

# nginx config: serve on 7860, proxy API calls to Flask on 5000
RUN echo 'server { \
    listen 7860; \
    location / { proxy_pass http://127.0.0.1:5000; proxy_set_header Host $host; proxy_read_timeout 300; proxy_send_timeout 300; } \
}' > /etc/nginx/sites-enabled/default

RUN echo '#!/bin/bash\nnginx\npython app.py' > /start.sh && chmod +x /start.sh

EXPOSE 7860

CMD ["/start.sh"]
