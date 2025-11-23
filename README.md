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

## 🚀 Features

### ✔ Implemented
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

### 🔧 In Progress
- **Full CRUD** (create, read, update, delete/disable)
- **SCIM Filtering** (`GET /Users?filter=userName eq "..."`)
- **SCIM PATCH** (replace, add, remove operations)
- **Automated tests** using pytest + in-memory SQLModel DB
- Postman collection for provisioning tests

---

## 🏗️ Architecture

