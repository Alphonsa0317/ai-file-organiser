<<<<<<< HEAD
📦 AI File Organizer + Monitoring Dashboard

A Dockerized, event-driven file management system that automatically organizes files, processes them asynchronously using workers, and provides real-time monitoring via Prometheus and Grafana.

🚀 Features
✅ Automatic file organization by type
✅ Real-time folder monitoring
✅ Asynchronous processing using Redis queues
✅ Duplicate detection (hash-based)
✅ Robust file handling (handles incomplete writes)
✅ REST API to view organized files
✅ Prometheus metrics for observability
✅ Grafana dashboard support
✅ Fully containerized with Docker Compose
✅ Cross-platform compatible (Linux / Windows / macOS)


🏗️ Architecture

+------------------+
          |   Watched Dir    |
          +------------------+
                    |
                    ▼
           +------------------+
           |   Watcher App    |
           +------------------+
                    |
                    ▼
              (Redis Queue)
                    |
        +-----------+-----------+
        |                       |
        ▼                       ▼
+----------------+      +----------------+
| Worker Service |      | Worker Service |
+----------------+      +----------------+
        |
        ▼
+------------------------+
| File Organizer Logic   |
+------------------------+
        |
        ▼
+------------------------+
| Organized Directory    |
+------------------------+

        ▲
        |
+------------------------+
| FastAPI Service        |
| (/files, /metrics)     |
+------------------------+

        ▲
        |
+------------------------+
| Prometheus + Grafana   |
+------------------------+


🛠️ Tech Stack

Backend: Python, FastAPI
Task Queue: Redis + RQ
File Monitoring: Watchdog
Monitoring: Prometheus, Grafana
Containerization: Docker, Docker Compose


📂 Project Structure
ai-file-organizer/
│
├── app/
│   ├── config.py
│   ├── main.py
│   ├── organizer.py
│   ├── watcher.py
│   ├── worker.py
│   └── utils.py
│
├── data/
│   ├── watched/
│   └── organized/
│
├── Dockerfile
├── docker-compose.yml
├── prometheus.yml
├── requirements.txt
└── .dockerignore



⚙️ Setup & Run
1. Clone Repository
Shellgit clone <your-repo-url>cd ai-file-organizerShow more lines

2. Run with Docker
Shelldocker compose up --buildShow more lines

3. Access Services

Service         URL
API         http://localhost:8000
Files API   http://localhost:8000/files
Metrics     http://localhost:8000/metrics
Prometheus  http://localhost:9090
Grafana     http://localhost:3000



📦 How It Works
Step 1 — File Detection

Watcher monitors data/watched/
Detects new files in real-time

Step 2 — Queueing

File processing jobs are pushed to Redis queue

Step 3 — Processing

Worker picks jobs
Categorizes files:

Images
Documents
Videos
Code
Archives
Executables

Step 4 — Organization

Moves files into data/organized/<category>/

Step 5 — Monitoring

Metrics exposed via /metrics
Prometheus scrapes data
Grafana visualizes system performance


📊 Metrics Tracked

processed_files_total → Total processed files
failed_files_total → Failed operations
file_processing_seconds → Processing time


🧪 Testing the System

Place any file into:

data/watched/

Example:

cp sample.pdf data/watched/

The file will be automatically moved to:

data/organized/Documents/


🐳 Docker Concepts Covered

Multi-container architecture
Volume mounting (host ↔ container)
Service communication (Docker network)
Health checks
Container orchestration via Docker Compose
Stateless vs stateful services


⚠️ Cross-Platform Notes

Aspect              Linux               Windows
File system     Case-sensitive          Case-insensitive
Performance     Faster volume I/O       Slower
Permissions     Strict                  Flexible



📈 Monitoring Setup (Grafana)

1.Open:

http://localhost:3000


2.Login:

Username: admin
Password: admin


3.Add data source:

URL: http://prometheus:9090


4.Create dashboard using:

processed_files_total
failed_files_total


🔒 Reliability Features

✅ Retry-safe Redis connections
✅ Duplicate file detection (MD5 hash)
✅ Safe handling of partially written files
✅ Memory-safe watcher (bounded cache)
✅ Error tracking and logging


📝 Example API Response
/files

JSON
{  "status": "success",  
"data": {    
    "Documents": ["file1.pdf", "report.docx"],    
    "Images": ["photo.jpg"]  
    }
}

📌 Future Improvements

File upload API
AI-based tagging and classification
Database logging (PostgreSQL)
Search functionality
CI/CD pipeline

=======

>>>>>>> c8323ebaa2376ac11165542805e1ab57063dbbae
