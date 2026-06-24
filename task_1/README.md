# Task 1: GitHub, Virtual Environment, and Linux Basics

## Description

This task demonstrates the setup of a Python project using GitHub, a virtual environment, and basic Linux commands. It includes a simple Python script, dependency management using `requirements.txt`, and documentation of the project setup process.

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/SnigdhaRoutray/Synergy_TP.git
cd Synergy_TP
```

### 2. Create a Virtual Environment

```bash
python3 -m venv task_1/venv
```

### 3. Activate the Virtual Environment

```bash
source task_1/venv/bin/activate
```

### 4. Install Required Packages

```bash
pip install -r task_1/requirements.txt
```

---

## Running the Python Script

From the root of the repository, run:

```bash
python task_1/src/hello.py
```

Expected output:

```text
Hello World
```

---

## Project Structure

```text
task_1/
├── README.md
├── requirements.txt
├── setup_log.md
├── linux_commands.md
├── src/
│   └── hello.py
└── data/
    └── sample.txt
```
