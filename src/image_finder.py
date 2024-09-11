import glob
import os
from typing import List

try:
    from src.config import FILEEXTENSIONS
except:
    from config import FILEEXTENSIONS

class ImagesFinder:
    def __init__(self, path: str) -> None:
        self.path = path
        self.all_images: List[str] = []
        extensions = FILEEXTENSIONS
        
        for ext in extensions:
            self.all_images.extend(glob.glob(os.path.join(self.path, ext)))

    def get_images(self) -> List[str]:
    
        return self.all_images