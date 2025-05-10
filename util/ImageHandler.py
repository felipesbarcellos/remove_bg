import os
import shutil
from rembg import remove
from PIL import Image

from util.constants import PATH_ORIGINALS, PATH_OUTPUT


class ImageHandler:
    def __init__(self, input_path: str):
        self.input_path = input_path
        print(f"Initializing ImageHandler with path: {input_path}")
        print(f"File exists: {os.path.exists(input_path)}")
        
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"File not found: {input_path}")
            
        (self.nome_sem_extensão, self.nome_com_extensão) = self._get_nome()
        self.output_path = self._get_output_path()
        self.originals_path = self._get_originals_path()
        self.image = Image.open(self.input_path)

    def _get_originals_path(self):
        return f"{PATH_ORIGINALS}{self.nome_com_extensão}"

    def _get_output_path(self) -> str:
        return f"{PATH_OUTPUT}{self.nome_sem_extensão}.png"

    def _get_nome(self):
        # Usa os.path para lidar com caminhos Windows e Unix
        nome_com_extensão = os.path.basename(self.input_path)
        nome_sem_extensão = os.path.splitext(nome_com_extensão)[0]
        return nome_sem_extensão, nome_com_extensão
        
    def remove_background(self) -> None:
        output = remove(self.image)
        self.image = output
        
    def add_background(self, color: str = "black") -> None:
        self.remove_background()
        output = Image.new(mode="RGBA", size=self.image.size, color=color)
        output.alpha_composite(self.image)
        self.image = output
    
    def save(self) -> None:
        self.image.save(self.output_path)
        if self.nome_sem_extensão != "teste":
            shutil.copy(self.input_path, self.originals_path)
            return
        shutil.copy(self.input_path, self.originals_path)
        
    def show(self) -> None:
        self.image.show()
        
    def resize_image(self, size: tuple|str = "half") -> None:
        if isinstance(size, tuple):
            size = (int(size[0]), int(size[1]))
        elif size == "half":
            size = tuple([int(i/2) for i in self.image.size])
        self.image = self.image.resize(size)


if __name__ == "__main__":
    pass