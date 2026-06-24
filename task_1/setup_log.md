# Setup Log

## Repository Setup

```bash
git clone https://github.com/SnigdhaRoutray/Synergy_TP.git
cd Synergy_TP
```

## Creating the Project Structure

```bash
mkdir task_1
mkdir task_1/data
mkdir task_1/src
```

## Virtual Environment Setup

```bash
python3 -m venv task_1/venv
source task_1/venv/bin/activate
```

## Installing Dependencies

```bash
pip install numpy
```

## Generating requirements.txt

```bash
pip freeze > task_1/requirements.txt
```

## Git Commands

```bash
git add .
git commit -m "Complete Task 1 setup"

git add task_1/README.md
git commit -m "Add Task 1 README"

git push
```
