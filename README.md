# hackathon
# GRIND GLITCH – Interstellar AI Tutor

A retro–space–gaming–themed AI tutor and diagnostics suite, powered by NVIDIA’s Llama AI core and GPU acceleration. Developed for hackathon use, **GRIND GLITCH** delivers:

- **Interactive AI Tutor Oracle**: Structured lessons, guided examples, and practice missions  
- **Cosmic Challenges**: Custom exam generator for “Foundations of Machine Learning” textbook  
- **Knowledge Forge**: Roadmap mode, chapter mode, assessments, and custom lessons  
- **Starship Diagnostics**: Real-time GPU engine monitoring and full GPU benchmark analysis  

---

## 🚀 Features

- **Retro Gaming & Space UI**: Custom CSS with floating UFOs, celebration animations, and neon-green styling  
- **NVIDIA API Integration**: High-quality LLM responses via `meta/llama-4-maverick-17b-128e-instruct`  
- **XP & Leveling System**: Gamified user progress tracking (XP, levels, chapters completed)  
- **Course Roadmap**: 17-chapter Machine Learning course with prerequisites and progress display  
- **Exam Generator**: AI-powered, difficulty-customizable exam creation and answer key  
- **Interactive Tutor**: Multi-step lessons—concept explanation, examples, practice, evaluation  
- **Diagnostics & Benchmarks**: GPU detection, memory stats, matrix multiplication speedups, memory bandwidth, RAPIDS/cuDF tests  

---

## 📋 Prerequisites

- **Python 3.8+**
- **NVIDIA GPU** (for full diagnostics; CuPy & RAPIDS optional for benchmarks)  
- **Environment Variable**:  
  ```bash
  export NVIDIA_API_KEY="nvapi-<your_key_here>"
