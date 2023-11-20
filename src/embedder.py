import os
import torch
import clip
from PIL import Image

class Embedder:

    def __init__(self, clipModel: str):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model, self.preprocess = clip.load(clipModel, device=self.device)


    def embedImage(self, file_path) -> tuple:
        try:
            image = self.preprocess(Image.open(file_path)).unsqueeze(0).to(self.device)
            with torch.no_grad():
                embedding = self.model.encode_image(image)
            return embedding
        except IOError:
            raise Exception("File to be embedded not an image")

    def embedText(self, input_text) -> torch.Tensor:
        text = clip.tokenize([input_text]).to(self.device)
        with torch.no_grad():
            return self.model.encode_text(text)
