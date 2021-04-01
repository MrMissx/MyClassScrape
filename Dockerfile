# Use python3.9 base image
FROM python:3.9

WORKDIR /ClassScraper/

RUN apt -qq update && apt -qq upgrade -y
RUN apt -qq install -y --no-install-recommends \
    curl \
    gcc \
    git \
    neofetch \
    wget

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python3", "-m", "bot"]
