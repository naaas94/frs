# JSONL Pipeline Endpoint

Pattern: ingestion_validation
Difficulty: medium

Build a FastAPI endpoint `POST /ingest` that accepts a list of JSONL lines in the request body and returns:

- Valid records after schema validation (`id: int`, `value: float`)
- Aggregates (`count`, `total_value`)
- Error list with line numbers and error type (`parse`, `validation`, `filter`)

Constraints:

- Records with `value <= 0` should be counted as filter errors.
- Preserve deterministic ordering in returned errors.
- Return a `422` only for malformed API payloads; JSONL issues must be returned in the response body.

Interview follow-up:

- How would you stream this for very large payloads?
- How would you avoid memory blowups?
