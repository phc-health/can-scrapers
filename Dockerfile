FROM prefecthq/prefect
WORKDIR /srv/can-scrapers
COPY requirements.txt setup.py can_tools .
RUN pip install -r requirements.txt && pip install -e .
