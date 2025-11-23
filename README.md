# SCIM 2.0 Provisioning API  
FastAPI • SQLModel • Pydantic • Azure Entra ID Integration

This project implements a **SCIM 2.0–compliant User resource API** designed for automated identity provisioning from **Azure Entra ID (Azure AD)** and other SCIM-capable identity providers.  
It follows RFC 7643 (Schemas) and RFC 7644 (Protocol).

The API uses a clean, layered architecture:
- **API Layer** — request validation & SCIM response formatting  
- **Service Layer** — business logic & SCIM operations  
- **Database Layer** — SQLModel ORM, relationships, and persistence  

This project is actively being expanded with full CRUD, filtering, and PATCH support.

---

## Features

### Implemented
- **SCIM 2.0 User Resource (RFC 7643)**
- Nested identity attributes:
  - `name` (formatted, givenName, familyName, etc.)
  - `phoneNumbers`
  - `manager`
- SQLModel relational models with:
  - One-to-one (e.g., User ↔ Name)
  - One-to-many (e.g., User ↔ PhoneNumbers)
- **User creation endpoint (`POST /Users`)**
- **User retrieval (`GET /Users/{id}`)**
- SCIM-compliant response formatting (schemas[], meta, null-handling)
- Defensive parsing for Entra ID’s inconsistent payloads  
  (e.g., unexpected fields during disable operations)

### In Progress
- **Full CRUD** (create, read, update, delete/disable)
- **SCIM Filtering** (`GET /Users?filter=userName eq "..."`)
- **SCIM PATCH** (replace, add, remove operations)
- **Automated tests** using pytest + in-memory SQLModel DB
- Postman collection for provisioning tests

---

## Architecture

app/
│
├── api/
│ ├── endpoints/ # FastAPI routers
│ ├── main.py # Application entry
│
├── services/ # Business logic (SCIM operations)
│
├── schemas/ # Pydantic models for request/response validation
│
│── user.py # SQLModel ORM models
│── database.py 



The project uses a **three-layer backend pattern**, ensuring clean separation between:
- HTTP interface  
- business logic  
- database persistence  

---

## 📡 API Endpoints (SCIM)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/Users` | Create a SCIM User |
| `GET`  | `/Users/{id}` | Retrieve a User by ID |
| `GET`  | `/Users?filter=...` | SCIM Filter (in progress) |
| `PATCH` | `/Users/{id}` | SCIM Patch (in progress) |
| `DELETE` | `/Users/{id}` | Soft-delete / disable user |

---

## 🗄️ Database Models (SQLModel)

The SCIM User resource maps to multiple SQLModel tables:

- `User`
- `Name`
- `PhoneNumber`
- `Manager`

Relationships:
- `User.name` → 1:1  
- `User.phone_numbers` → 1:N  
- `User.manager` → 1:1 optional  

Foreign keys and constraints maintain SCIM consistency and data integrity.

---

## 🔒 SCIM Compliance Details

The API returns responses wrapped in the correct SCIM structure:

```json
{
  "schemas": ["urn:ietf:params:scim:schemas:core:2.0:User"],
  "id": 123,
  "userName": "...",
  "name": { "...": "..." },
  "meta": {
    "resourceType": "User",
    "created": "2025-11-04T08:21:00Z",
    "lastModified": "2025-11-04T08:21:00Z",
    "location": "/Users/123"
  }
}

Testing
Unit tests (in progress) use:
pytest
FastAPI TestClient
SQLModel in-memory SQLite DB
This ensures:
isolated test environments
deterministic behavior
no external dependencies
Example scaffold:

def test_create_user():
    response = client.post("/Users", json={...})
    assert response.status_code == 201



📬 Future Enhancements
Group resource support (/Groups)
Token-based auth for management endpoints
Pagination & sorting
SCIM bulk operations
Dockerfile + compose for local provisioning


