

# AudioScribe
*A multimodal AI that reads the physical world aloud, empowering independence for the visually impaired.*

![Hackathon Project](https://img.shields.io/badge/Project-24--Hour%20Hackathon-blueviolet)
![Status](https://img.shields.io/badge/Status-Proof%20of%20Concept-success)

## The Problem
For millions of visually impaired individuals, the digital world has become increasingly accessible thanks to screen readers. However, the physical world remains a significant challenge. Simple, everyday tasks that sighted individuals take for granted—such as identifying the correct medication, reading cooking instructions on a food package, or understanding a utility bill—present major barriers to safety and independence. The core issue is not just reading text, but understanding its context and importance.

## Our Solution: AudioScribe
AudioScribe is a proof-of-concept for a multimodal AI assistant designed to bridge the gap between the physical and digital worlds.

It allows a user to take a photo of any object with text and receive a clear, context-aware audio summary of the most important information. It doesn't just read the text; it acts as a specialized transcriber, identifying the object, prioritizing critical information like product names and warnings, and structuring the output in a way that is immediately useful for an audio-first experience.

### Key Features (Proof of Concept)
*   **Accessible-First Interface:** A clean, simple, and screen-reader-friendly web interface for uploading images.
*   **Intelligent Analysis:** Utilizes a powerful, instruction-tuned Vision-Language Model (`microsoft/Phi-3-vision`) to perform contextual analysis, not just raw OCR.
*   **Structured Audio Output:** A professional, multi-part prompt forces the AI to structure its response in a predictable and useful format, ideal for audio consumption.
*   **Instant Text-to-Speech:** Uses the browser's native Web Speech API to provide immediate audio feedback.
*   **Interactive Follow-up:** Includes a "Read That Again" feature, demonstrating the potential for a more interactive, conversational experience.

## Tech Stack
Our architecture is a decoupled client-server application built with modern, open-source technologies.

| Area | Technology | Description |
|---|---|---|
| **Frontend** | Vanilla HTML, CSS, JavaScript | A lightweight, fast, and accessible user interface. |
| | Web Speech API | Browser-native text-to-speech for instant audio output. |
| | ARIA Attributes | Ensures the application is fully navigable with screen readers. |
| **Backend** | Python & FastAPI | A high-performance, asynchronous API for handling image uploads. |
| | Uvicorn | The ASGI server running our FastAPI application. |
| | `uv` | A high-speed package manager and virtual environment tool. |
| **AI Core** | Hugging Face `transformers` | The library for downloading and running our AI model. |
| | `microsoft/Phi-3-vision` | A state-of-the-art, instruction-tuned Vision-Language Model. |
| | PyTorch | The deep learning framework powering the AI model. |
| | NVIDIA CUDA / `flash-attn` | **(Recommended)** For massive performance gains via GPU acceleration. |


## Getting Started
### Prerequisites
*   Python 3.12
*   `uv` (can be installed with `pip install uv`)
*   **(Recommended for Performance)** An NVIDIA GPU with the [NVIDIA CUDA Toolkit 12.1](https://developer.nvidia.com/cuda-12-1-0-download-archive) installed.

### Backend Setup
1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd AudioScribe/backend
    ```
2.  **Create and activate the virtual environment:**
    ```powershell
    # For CPU-only
    uv venv --python 3.12
    .venv\Scripts\Activate.ps1
    ```
3.  **Install dependencies (GPU RECOMMENDED):**
    *   **For GPU (RTX 30/40 series recommended):**
        ```powershell
        # 1. Install CUDA-enabled PyTorch
        uv pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
        # 2. Install all other packages
        uv pip install fastapi uvicorn python-multipart Pillow "transformers>=4.41.2" accelerate flash-attn
        ```
    *   **For CPU-only:**
        *Ensure your `ai_core.py` is configured for CPU as discussed in the project journey.*
        ```powershell
        uv pip install fastapi uvicorn python-multipart Pillow "transformers>=4.41.2" torch accelerate
        ```
4.  **Run the server:**
    The first run will download the large AI model. Please be patient.
    ```bash
    uvicorn main:app --reload
    ```
    The backend will be running at `http://127.0.0.1:8000`.

### Frontend Setup
1.  Navigate to the `frontend` directory.
2.  Open the `index.html` file in any modern web browser.

---



#### 1. The Framing Problem
*   **The Challenge:** How does a visually impaired user know if they are aiming the camera correctly to capture the product label? The web app has no access to a live camera feed to provide guidance.
*   **Real-World Mitigation:** This is solved by evolving the project into a **native mobile application**. A native app can provide real-time audio and haptic feedback, using a simple on-device object detection model to guide the user: *"Move left... a bit closer... hold still."* This creates a guided capture experience, ensuring a perfect photo every time.

#### 2. The Selection Problem
*   **The Challenge:** The web app relies on the user selecting the correct photo from their device's gallery, which is often an inaccessible grid of unlabelled images. Our PoC assumes the user is analyzing the "most recent" photo.
*   **Real-World Mitigation:** The native mobile app also solves this. By integrating an **in-app camera**, we eliminate the need for the user to ever interact with their photo gallery. The workflow becomes seamless: open the app, capture the image with guidance, and get the analysis instantly.

## The Vision: Next Steps
This PoC is the foundation for a complete assistive tool. The roadmap for AudioScribe includes:
*   **Developing the Native Mobile App:** Porting the core logic to a Swift (iOS) and Kotlin (Android) application to implement the guided capture and in-app camera solutions.
*   **Implementing True Conversational AI:** Moving beyond a "Read That Again" button to a voice-activated follow-up system. The user could ask questions like, *"What are the active ingredients?"* or *"Read me the warnings again."*
*   **Offline Mode:** Using smaller, distilled on-device models for essential tasks (like basic text reading) when an internet connection is not available.
*   **Multi-Language Support:** Expanding the model's capability and the user interface to serve a global audience.