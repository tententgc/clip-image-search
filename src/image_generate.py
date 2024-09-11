import clip
import torch
import chromadb
from chromadb import Settings

import time
from PIL import Image
from typing import List
from pathlib import Path

try:
    from src.config import MODEL, FILE_IMAGES, NAME_IMAGES, SPACE, METHOD
except ImportError:
    from config import MODEL, FILE_IMAGES, NAME_IMAGES, SPACE, METHOD


class ClipModel:
    def __init__(self, images: List[str]) -> None:
        self.images = images
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model, self.preprocess = clip.load(MODEL, device=self.device)

        self.chroma_client = self._initialize_chroma_client()
        self.image_collection = self.create_vector_database()

        self.add_image_to_database()

    def _initialize_chroma_client(self) -> chromadb.PersistentClient:
        client = chromadb.PersistentClient(FILE_IMAGES, settings=Settings(allow_reset=True))
        client.reset()
        return client

    def create_vector_database(self) -> chromadb.Collection:
        return self.chroma_client.create_collection(
            NAME_IMAGES,
            metadata={SPACE: METHOD}
        )

    def add_image_to_database(self) -> None:
        for idx, image_path in enumerate(self.images, start=1):
            image = self.preprocess(Image.open(image_path)).unsqueeze(0).to(self.device)
            with torch.no_grad():
                image_features = self.model.encode_image(image).cpu().numpy().tolist()

            self.image_collection.add(
                ids=str(idx),
                embeddings=image_features,
                metadatas={"path": image_path, "name": Path(image_path).name}
            )

    def search_image(self, search_text: str) -> List[dict]:
        text = clip.tokenize(search_text).to(self.device)
        with torch.no_grad():
            text_features = self.model.encode_text(text).cpu().numpy()

        search_result = self.image_collection.query(
            query_embeddings=text_features.tolist(),
            n_results=5
        )
        return search_result['metadatas'][0]