# Text-Search-Image

This project implements an efficient image search system using the CLIP (Contrastive Language-Image Pre-training) model. It allows users to search for images with natural language queries, offering a seamless and intuitive way to interact with image datasets.

## Features

- **Image Processing:** Load and process images from a specified directory.
- **CLIP Model Integration:** Encode images into embeddings using the CLIP model for precise image-to-text matching.
- **Vector Database:** Store image embeddings in ChromaDB for fast and scalable retrieval.
- **Text-Based Search:** Find relevant images based on natural language queries.
- **User-Friendly Interface:** A simple graphical interface for easy image search and browsing.

## Requirements

- **Python:** Version 3.9.16
- **Flet:** For building the graphical user interface (GUI).
- **CLIP Model:** To generate high-quality embeddings from images.
- **ChromaDB:** For efficient storage and retrieval of image embeddings.

## Installation

Follow these steps to set up and run the project on your local machine:

1. **Clone the Repository:**
    ```bash
    git clone https://github.com/tententgc/clip-image-search.git
    cd clip-image-search
    ```

2. **Set Up a Virtual Environment** (optional but recommended):
    ```bash
    python -m venv test
    source test/bin/activate  # On Windows, use `test\Scripts\activate`
    ```

3. **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. **Run the Application:**
    ```bash
    python run.py
    ```

2. **Using the Interface:**
   - Enter the path to the directory containing your images.
   - Click the "Add" button to load and process the images into the system.
   - Enter a text query into the search box.
   - Click the "Search" button to retrieve matching images.

## Project Structure

```
text_search_image_clip/
├── assets/                # Contains static assets like images and icons
├── data/                  # Stores processed images and embeddings
├── src/
│   ├── config.py          # Configuration settings for the application
│   ├── image_finder.py    # Handles image search functionality
│   └── image_generator.py # Manages image encoding and embedding generation
├── README.md              # Project documentation
├── requirements.txt       # List of dependencies
└── run.py                 # Main script to run the application
```

