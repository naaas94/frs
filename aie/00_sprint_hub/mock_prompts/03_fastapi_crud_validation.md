# FastAPI CRUD With Validation

Pattern: fastapi_basics
Difficulty: medium

Design and implement a minimal in-memory ticket API:

- `POST /tickets` create ticket
- `GET /tickets/{ticket_id}` read ticket
- `GET /tickets?status=open` filter tickets

Requirements:

- Use Pydantic request/response models.
- Return proper HTTP errors for not found and invalid states.
- Include `created_at` and `updated_at` fields.

Interview follow-up:

- How would this change with a real DB?
- What indexes would you add first?
