# https://docs.bentoml.org/en/latest/use-cases/embeddings/clip-embeddings.html
MODEL = "ViT-B/32"

FILE_IMAGES = "image_search.db"
NAME_IMAGES = "image"
SPACE = "hnsw:space"
METHOD = "cosine"

FILEEXTENSIONS = ['*.jpg', '*.png', '*.jpeg']