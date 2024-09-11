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
except:
    from config import MODEL, FILE_IMAGES, NAME_IMAGES, SPACE, METHOD


class ClipModel:
    """
        This class is used to search images using CLIP model and store the image features in ChromaDB.

        Attributes:
            images (List[str]): List of image paths to process.
            device (str): Device to use for processing ('cuda' or 'cpu').
            model: CLIP model.
            preprocess: CLIP preprocessing function.
            chroma_client: ChromaDB client.
            image_collection: ChromaDB collection for storing image embeddings.

        Methods:
            create_vector_database(): Create a new collection in ChromaDB.
            add_image_to_database(): Process images and add their embeddings to the database.
            search_image(search_text: str): Search for images based on text query.
    """

    def __init__(self, images: List[str]) -> None:
        start_time = time.time()
        self.images = images
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model, self.preprocess = clip.load(MODEL, device=self.device)
        
        self.chroma_client = chromadb.PersistentClient(
            FILE_IMAGES,
            settings=Settings(allow_reset=True)
        )
        self.chroma_client.reset()
        
        self.create_vector_database()
        self.add_image_to_database()

        print("Successfully loaded model")
        print(f"Time taken to load model: {time.time() - start_time:.2f} seconds")
        print(f"Device process is: {self.device}")

    def create_vector_database(self) -> None:
        """Create a new collection in ChromaDB for storing image embeddings."""
        self.image_collection = self.chroma_client.create_collection(
            NAME_IMAGES,
            metadata={SPACE: METHOD}
        )

    def add_image_to_database(self) -> None:
        """Process images and add their embeddings to the database."""
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
        # """
        #     Search for images based on text query.

        #     Args:
        #         search_text (str): The text to search for.

        #     Returns:
        #         List[dict]: A list of metadata for the top 5 matching images.
        # """
        text = clip.tokenize(search_text).to(self.device)
        with torch.no_grad():
            text_features = self.model.encode_text(text).cpu().numpy()

        search_result = self.image_collection.query(
            query_embeddings=text_features.tolist(),
            n_results=5
        )
        return search_result['metadatas'][0]

    # Commented out alternative search_image method
    # def search_image(self, search_text: str, threshold: float = 0.5) -> List[dict]:
    #     text = clip.tokenize(search_text).to(self.device)
    #     with torch.no_grad():
    #         text_features = self.model.encode_text(text).cpu().numpy()

    #     search_result = self.image_collection.query(
    #         query_embeddings=text_features.tolist(),
    #         where={"$and": [{"similarity": {"$gte": threshold}}]},
    #         include=["metadatas", "distances"]
    #     )
        
    #     results = [
    #         {**metadata, 'similarity': 1 - distance}
    #         for metadata, distance in zip(search_result['metadatas'][0], search_result['distances'][0])
    #     ]
        
    #     return sorted(results, key=lambda x: x['similarity'], reverse=True)