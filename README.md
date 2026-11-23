# Trino AI Explorer

An incremental proof of concept for exploring lakehouse data using natural language.
The eventual flow is Streamlit → LLM → Trino → Polaris → Iceberg → S3-compatible
storage, with SQL, results and Plotly visualisations displayed in the UI.

## Current milestone: local Trino integration

The app offers two data sources: an in-memory SQLite demo and a local Trino
Iceberg table registered in Polaris and stored in RustFS. Both modes match the
example questions shown in the UI to predefined SQL and display the SQL,
results and a chart. Matching ignores case and extra whitespace; other questions
are not supported yet.

**This is not yet an LLM integration.** Trino mode supports three questions;
the daily revenue question is only available in the SQLite demo because the
Trino sample table has no date column.

## Project structure

```text
app.py              Streamlit interface
explorer/demo.py    Example questions, sample data and local query execution
explorer/charts.py  Automatic chart selection
explorer/trino_client.py  Local Trino query execution
tests/              Focused tests
requirements.txt    Application dependencies
infra/              Local Trino, Polaris and S3-compatible storage setup
```

## Run locally

With Python 3.10 or later:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
streamlit run app.py
```

Select **Local demo** to run without external services. To use **Trino**, first
start and initialize the local lakehouse below, then select **Trino**, choose an
example question and select **Explore**. No API keys are needed.

Run the demo tests with:

```sh
python -m unittest discover -s tests
```

## Local lakehouse

The local stack runs Trino, Apache Polaris and RustFS (S3-compatible storage)
with Docker Compose. This setup is for mock data only and is not production-ready.

With Docker Desktop running, generate local credentials once:

```sh
umask 077
printf 'STORAGE_ACCESS_KEY=%s\nSTORAGE_SECRET_KEY=%s\nPOLARIS_CLIENT_ID=%s\nPOLARIS_CLIENT_SECRET=%s\n' \
  "$(openssl rand -hex 12)" "$(openssl rand -hex 24)" \
  "$(openssl rand -hex 12)" "$(openssl rand -hex 24)" > infra/.env
```

The generated file is ignored by Git; do not share or commit it. Start the
services and create a sample Iceberg table:

```sh
docker compose -f infra/compose.yaml up -d --wait
docker compose -f infra/compose.yaml exec -T trino trino < infra/sample.sql
```

The last command prints revenue by region. Run it again without duplicating
data, or open the Trino UI at http://localhost:8080 to explore the `iceberg`
catalog. Polaris is available at http://localhost:8181.

**Data is disposable:** Polaris uses an in-memory catalog. Restarting services
can lose the catalog. The following command stops the stack and deletes its
containers and storage volume, including all sample data:

```sh
docker compose -f infra/compose.yaml down --volumes
```

To start fresh, run the two startup commands again. The stack uses generated
local credentials, but exposes an unauthenticated Trino endpoint on localhost;
do not use it for real data or expose it to a network.

## Next milestones

1. Add OpenAI or Azure OpenAI to generate SQL from unrestricted questions, with
   explicit safeguards and a read-only Trino account.
2. Improve the local stack's persistence and replace disposable credentials.

LLM-generated SQL is untrusted. Before connecting it to real data, enforce query
and access restrictions in Trino rather than relying solely on prompt instructions.
