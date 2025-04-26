## 🔥 BookSage AI

**Multi-Method Book Recommendation System**

![Image](https://github.com/user-attachments/assets/bc72c776-4cc8-4966-a678-00efaee64334)
---

## 🎯 Project Goal

Provide personalized book recommendations by combining **Collaborative Filtering** and **Content-Based Filtering** techniques, ensuring high accuracy even when user interaction data is sparse.

---

# 📂 Project Structure for **BookSage AI**

```bash
BookSage-AI/
│
├── app/                            
│   ├── __init__.py                 
│   ├── config.py                 
│   ├── data_loader.py   
│   ├── utils.py   
│   ├── recommender.py          
│   ├── logger.py                     
│   └── config.py                     
│
├── main.py                            # Streamlit frontend main app
│
├── main/                              # all in one code
│   ├── main.py
│
├── data/                              # Data Folder
│   ├── BX-Books.csv                    
│   ├── BX-Book-Ratings.csv            
│   └── BX-Users.csv 
│
├── jupyter/                            
│   ├── experiment.ipynb                                    
│
├── tests/                             # Test Cases (Future Scope)
│   ├── test_main.py
│
├── .github/                           # GitHub specific files
│   └── workflows/
│       └── main.yml                   # GitHub Actions CI/CD workflow file
│
├── Dockerfile                         # Docker build file
├── render.yml                         # render deploy file
├── requirements.txt                   # Python dependencies
├── setup.py                           # Python setup file
├── README.md                          # Project Documentation
├── .gitignore                         # Files/folders to ignore in GitHub repo
├── app.png                            # Demo
│
└── LICENSE                            # License
```

---

## 🧠 Core Technologies

| Technology         | Purpose                                    |
|---------------------|--------------------------------------------|
| Python 3.11         | Core Programming Language                 |
| Streamlit           | Frontend Web Application Framework        |
| Scikit-learn        | Machine Learning Model Building           |
| Pandas, NumPy       | Data Manipulation                         |
| Docker              | Containerization                          |
| GitHub Actions      | CI/CD Automation                          |
| Logging (Python)    | Application Monitoring                    |

---

## 📦 Major Components

| Component                     | Description                                                  |
|--------------------------------|--------------------------------------------------------------|
| Data Loader                    | Data reading and preprocessing                              |
| Content-Based Recommender      | Recommend books based on metadata similarities              |
| Collaborative Filtering Engine | Recommend books based on user preferences                   |
| Hybrid Recommendation Engine   | Combines content-based and collaborative outputs            |
| Streamlit Frontend             | Interactive UI for Book Recommendations                     |
| Centralized Logger             | Real-time Monitoring and Debugging Support                  |
| CI/CD Pipeline (GitHub Actions)| Automated Testing, Docker Build, Deployment Automation      |

---

## 🌐 Deployment Plan

### Local Development

- Virtual Environment setup
- Running via `main run`
- Local Logging for debugging

### Dockerized Deployment

- Dockerfile included
- Docker Build and Run commands
- Ideal for consistent environments across development, staging, and production.

### CI/CD Pipeline (Implemented)

- **GitHub Actions Workflow**:
  - On Push or Pull Request:
    - Linting and Code Quality Checks
    - Run Unit Tests (Optional pytest Integration)
    - Build Docker Image
    - Push to DockerHub (Private/Public Repo)
    - Deploy to Cloud (Future ready)
  
> ✅ Future Scope: Auto-deploy to AWS ECS / Azure App Service / GCP Cloud Run.

---

## 🛠️ How to Setup (Locally)

```bash
# Clone the Repository
git clone https://github.com/Md-Emon-Hasan/BookSage-AI.git
cd hybrid-book-recommender

# Setup Virtual Environment
python -m venv venv
source venv/bin/activate

# Install Dependencies
pip install -r requirements.txt

# Run Streamlit App
streamlit run main.py
```

---

## 🐳 How to Setup (Dockerized)

```bash
# Clone the Repository
git clone https://github.com/Md-Emon-Hasan/BookSage-AI.git
cd BookSage-AI

# Build Docker Image
docker build -t booksage-ai .

# Run Docker Container
docker run -p 8501:8501 booksage-ai
```

---

## 🛡️ Logging Mechanism

- Centralized Logger module with customizable Log Levels
- Logs critical events like data loading issues, recommendation failures, server errors
- Supports both **Console Output** and **File Saving**

Example Usage:
```python
from app.logger import get_logger
logger = get_logger()

logger.info("User requested new book recommendations.")
logger.error("Failed to generate collaborative recommendations.")
```

---

## 🧪 Test Setup (Optional)

- Currently no pytest implemented.
- Future Scope:
  - Add Unit Tests for each recommender engine.
  - Integrate Test Execution in CI/CD.

---

## ⚙️ CI/CD Pipeline (Full Flow)

| Step                           | Tool          | Purpose                              |
|---------------------------------|---------------|--------------------------------------|
| Code Push / Pull Request        | GitHub        | Trigger CI/CD Workflow               |
| Code Quality & Linting          | flake8 (optional) | Ensure Coding Standards            |
| Unit Testing (Future Scope)     | pytest        | Run All Test Cases                   |
| Build Docker Image              | Docker        | Package the Application              |
| Push Image to DockerHub         | GitHub Actions| Automatic Push after Build           |
| Deploy to Server (future ready) | GitHub Actions| Auto-deploy on Cloud or VPS server    |

---
**Sample GitHub Actions Workflow (`.github/workflows/main.yml`)**
```yaml
name: Docker Image CI-CD

on:
  push:
    branches: [ "master" ]
  pull_request:
    branches: [ "master" ]

jobs:
  build:

    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.x'

    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v2

    - name: Cache Docker layers
      uses: actions/cache@v3
      with:
        path: /tmp/.buildx-cache
        key: ${{ runner.os }}-buildx-${{ github.sha }}
        restore-keys: |
          ${{ runner.os }}-buildx-

    - name: Build Docker image
      run: docker build -t BookSage-AI .

    - name: Test the application (Run tests inside container)
      run: docker run --rm BookSage-AI pytest tests/
```

---

## 📑 Extra Features

| Feature                    | Details                                              |
|-----------------------------|------------------------------------------------------|
| Adjustable Weighting        | User can adjust importance between Collaborative vs Content-Based results dynamically |
| Popularity Fallback System  | If recommendation engines fail, fallback to Top-rated Books |
| Modular Code Structure      | Easier Maintenance and Testing                      |
| Scalability Ready           | Optimized for future Cloud Hosting                  |

---


# 🚀 Conclusion

The **Hybrid Book Recommendation System** is a **production-ready, scalable**, and **cloud-deployable** application blending the strengths of multiple recommendation techniques, backed by a complete CI/CD pipeline ensuring continuous improvement and smooth deployments.

---
  
✍️ **Prepared by:**  

**Md Emon Hasan**  
📧 **Email:** iconicemon01@gmail.com  
💬 **WhatsApp:** [+8801834363533](https://wa.me/8801834363533)  
🔗 **GitHub:** [Md-Emon-Hasan](https://github.com/Md-Emon-Hasan)  
🔗 **LinkedIn:** [Md Emon Hasan](https://www.linkedin.com/in/md-emon-hasan)  
🔗 **Facebook:** [Md Emon Hasan](https://www.facebook.com/mdemon.hasan2001/)

---
