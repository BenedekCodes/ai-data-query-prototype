# Trino AI Explorer

AI-powered natural language querying and visualisation for Trino-based data platforms using Apache Iceberg, Polaris, and mock datasets.

## Overview

Trino AI Explorer is a prototype application that allows users to query data using natural language. User prompts are translated into SQL, executed through Trino, and the results are returned as interactive visualisations.

The project demonstrates how AI can simplify data exploration across modern lakehouse architectures built on Apache Iceberg and Polaris.

## Objectives

- Natural language → SQL generation
- Query execution through Trino
- Apache Iceberg table support
- Polaris catalog integration
- Dynamic visualisations and dashboards
- Demonstration using mock data

## Architecture

- Frontend: Streamlit
- Query Engine: Trino
- Table Format: Apache Iceberg
- Catalog: Polaris
- Storage: S3-compatible object storage
- AI Layer: LLM-powered SQL generation

## Status

🚧 Prototype / Proof of Concept
