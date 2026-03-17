# 🚀 Report: Containerized Web Application with PostgreSQL using Docker Compose and Macvlan

**Date:** 16 March 2026

---

## 📑 Table of Contents

1. Objective
2. System Architecture & Design
3. Implementation Details
4. Dockerization Strategy & Build Optimization
5. Networking: Macvlan Configuration
6. Orchestration with Docker Compose
7. Verification and Proofs
8. Conclusion

---

# 1. Objective

The objective of this project is to design, containerize, and deploy a production-ready web application using:

* **FastAPI (Python)** as backend
* **PostgreSQL** as database
* **Docker & Docker Compose** for containerization and orchestration
* **Macvlan networking** for LAN-level container communication

The system demonstrates:

* Production-ready Docker images
* Container networking concepts
* Persistent storage using volumes
* Service orchestration

---

# 2. System Architecture & Design

## 🔹 Component Overview

The system consists of three main components:

1. **Client**

   * Browser or Postman
   * Sends HTTP requests

2. **Backend Container (FastAPI)**

   * Handles API requests
   * Connects to PostgreSQL

3. **Database Container (PostgreSQL)**

   * Stores application data
   * Uses persistent volume

---

## 🔹 Architecture Diagram

```
Client (Browser/Postman)
        ↓
FastAPI Backend Container
        ↓
PostgreSQL Container
        ↓
Docker Volume (Persistent Storage)
```

---

# 3. Implementation Details

## 🔹 Backend API (FastAPI)

The FastAPI backend provides:

* `GET /health` → Health check
* `POST /users` → Insert user
* `GET /users` → Fetch all users

The backend connects to PostgreSQL using environment variables:

```
DB_HOST
DB_NAME
DB_USER
DB_PASSWORD
```

The table is automatically created on startup using SQL.

📸 ![Docker Output](screenshots/screenshot (579).png)

---

## 🔹 Database (PostgreSQL)

* Custom Dockerfile used (not default image directly)
* Table auto-created using `init.sql`

```sql
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name TEXT,
    email TEXT
);
```

---

# 4. Dockerization Strategy & Build Optimization

## 🔹 Backend Dockerfile

* Base image: `python:3.11-slim`
* Uses non-root user (`appuser`)
* Minimal layers
* Optimized dependency installation

## 🔹 Database Dockerfile

* Base image: `postgres:15-alpine`
* Copies `init.sql` for auto table creation

---

## 🔹 Build Optimization Techniques

* Slim/alpine images → smaller size
* `.dockerignore` → avoids unnecessary files
* Layer caching → faster builds
* Non-root user → improved security

---

## 🔹 Image Size Comparison

Command used:

```bash
docker images
```

| Image             | Size    |
| ----------------- | ------- |
| Backend (slim)    | Small   |
| Database (alpine) | Reduced |

 ![Docker Output](screenshots/Screenshot(582).png)


---

# 5. Networking: Macvlan Configuration

## 🔹 Network Creation Command

```bash
docker network create -d macvlan \
--subnet=192.168.1.0/24 \
--gateway=192.168.1.1 \
-o parent=eth0 \
mymacvlan
```

## 🔹 Static IP Assignment

* Backend → 192.168.1.50
* Database → 192.168.1.51

---

## 🔹 Host Isolation Issue

Macvlan isolates containers from the host system:

* Containers are not accessible via `localhost`
* Host cannot communicate directly

### ✔ Solution

* Used **bridge network for testing**
* Used **macvlan for demonstration and screenshots**

 ![Docker Output](screenshots/screenshot (583).png)

 ![Docker Output](screenshots/screenshot (589).png)

---

# 6. Orchestration with Docker Compose

The `docker-compose.yml` file:

* Defines backend and database services
* Uses environment variables
* Uses named volume (`postgres_data`)
* Includes restart policy
* Includes healthcheck
* Uses depends_on

---
 ![Docker Output](screenshots/screenshot (598).png)

---

# 7. Verification and Proofs

## 🔹 1. Running Containers

```bash
docker ps
```
![Docker Output](screenshots/Screenshot(606).png)
---

## 🔹 2. Network Inspection

```bash
docker network inspect mymacvlan
```

![Docker Output](screenshots/screenshot (583).png)

---

## 🔹 3. Container IP Verification

```bash
docker inspect fastapi_container
```

![Docker Output](screenshots/screenshot (589).png)
![Docker Output](screenshots/screenshot (595).png)

---

## 🔹 4. Volume Persistence Test

Steps:

1. Insert data via POST request
2. Stop containers

```bash
docker compose down
```

3. Restart containers

```bash
docker compose up -d
```

4. Fetch data → still present

![Docker Output](screenshots/screenshot (601).png)
![Docker Output](screenshots/screenshot (602).png)
![Docker Output](screenshots/screenshot (603).png)
![Docker Output](screenshots/screenshot (604).png)
![Docker Output](screenshots/screenshot (605).png)
## 🔹 Volume Persistence Test

A volume persistence test was performed to verify that data remains intact even after container restart.

### Steps Performed:

1. Inserted data into the database using POST request (`/users`)
2. Stopped containers using:
   ```bash
   docker compose down

---

## 🔹 5. API Testing

Access:

```
http://localhost:8000/docs
```

![Docker Output](screenshots/screenshot (579).png)

---

# 8. Macvlan vs Ipvlan

| Feature     | Macvlan        | Ipvlan                 |
| ----------- | -------------- | ---------------------- |
| MAC Address | Unique         | Shared                 |
| Isolation   | High           | Medium                 |
| Host Access | Not allowed    | Allowed                |
| Use Case    | LAN simulation | Lightweight networking |

---

# 9. Conclusion

This project successfully demonstrates:

* Containerization using Docker
* Service orchestration using Docker Compose
* Persistent storage using volumes
* Networking using macvlan
* Production-ready Docker practices

The system meets all functional and architectural requirements and provides a scalable and efficient containerized application setup.

---

## 🔗 GitHub Repository

https://github.com/harshitachabaria24/Containerization_and_Devops
