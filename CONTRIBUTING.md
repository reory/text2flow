# Contributing to Text2Flow 📊

Thank you for your interest in contributing to **Text2Flow**! We welcome contributions to help improve our FastAPI and Graphviz powered text-to-diagram generation engine.

---

## 📑 Table of Contents
- [Code of Conduct](#code-of-conduct)
- [System Prerequisites](#-system-prerequisites)
- [How Can I Contribute?](#-how-can-i-contribute)
- [Development Setup](#-development-setup)
- [Testing Guidelines](#-testing-guidelines)
- [Project Architecture](#-project-architecture)
- [Style Guide & Code Standards](#-style-guide--code-standards)

---

## Code of Conduct
By participating in this project, you agree to foster an open, welcoming, and respectful environment for all contributors.

---

## ⚙️ System Prerequisites

Because Text2Flow relies on native Graphviz rendering engines, you **must install the Graphviz binaries** on your operating system before running or developing locally:

* **Windows**: Download the installer from the official site. Make sure to check **"Add Graphviz to system PATH"** during installation.
* **macOS**:
  ```bash
  brew install graphviz
  ```
* **Linux (Ubuntu/Debian)**:
  ```bash
  sudo apt update && sudo apt install graphviz
  ```

---

## 🛠️ How Can I Contribute?

### 🐛 Reporting Bugs
If you encounter syntax parsing failures, rendering timeouts, or FastAPI runtime exceptions:
* Search the **Issues** tab to verify it hasn't been reported yet.
* If not, open a new issue detailing:
  * Your operating system and Graphviz version (`dot -V`).
  * The exact text syntax input that caused the issue.
  * Python/FastAPI server logs or console tracebacks.

### ✨ Suggesting Enhancements & Roadmap Features
We welcome proposals for new shape definitions, color palettes, or feature implementations! Check our [Roadmap Features](README.md#-roadmap-features) in `README.md` first. Popular topics include:
* **Real-time Live Preview** with async debounce logic.
* **Theme Preset Engines** (Cyberpunk, Solarized, Dark Mode).
* **Multi-Engine Layouts** (`circo`, `neato`, `twopi`).
* Open an issue to discuss your proposal before starting major work.

### 🛠️ Pull Requests
1. **Fork** the repository and clone your fork locally.
2. Create a feature branch off `main`:
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. Implement your changes and verify that all test suites pass.
4. **Commit** your work with clear, descriptive commit messages:
   ```bash
   git commit -m 'feat: add circo layout engine support to renderer service'
   ```
5. **Push** your branch:
   ```bash
   git push origin feature/AmazingFeature
   ```
6. Submit a **Pull Request** against the upstream `main` branch.

---

## 🚀 Development Setup

1. **Clone and Navigate**:
```bash
git clone https://github.com/reory/text2flow.git
cd text2flow
```

2. **Set Up Virtual Environment**:
```bash
python -m venv venv
# Windows PowerShell:
.\venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

3. **Sync Dependencies:**
uv will automatically create the virtual environment and install all pinned dependencies:
```bash
uv sync
```

4. **Launch Development Server**:
```bash
uv run uvicorn app.main:app --reload
```

5. **Launch Desktop GUI:**
```bash
uv run python gui_app.py
```

*Access the editor interface locally at `http://127.0.0.1:8000`.*

6. **Codebase Aggregation (pyragify)**:
If preparing context files for LLM analysis or documentation:
```bash
uv run python -m pyragify --config-file config.yaml
```

---

## 🧪 Testing Guidelines

We use `pytest` to validate router endpoints, arrow parsing logic, and Graphviz render pipelines. Ensure all unit and integration tests pass before opening a PR:

```bash
uv run pytest
```

When adding new parsing capabilities or layout engines, please write corresponding test cases under the `tests/` directory.

---

## 📏 Style Guide & Code Standards
* **Python**: Adhere to PEP 8 standard formatting and type hints (`pydantic` models where applicable).
* **Decoupling**: Keep parsing and rendering logic strictly inside `app/services/` and offload HTTP handling to `app/routers/`.
* **Frontend**: Keep vanilla JavaScript (`app/static/js/app.js`) clean, efficient, and free of heavy external frame libraries.

---

Thank you for building better workflow diagrams with Text2Flow! 😊