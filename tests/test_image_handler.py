from util.ImageHandler import ImageHandler
from util.constants import TEST_FILE, PATH_INPUT
from loguru import logger
from PIL import Image

def image_handler() -> ImageHandler:
    input_path = f"{PATH_INPUT}{TEST_FILE}"
    return ImageHandler(input_path)
    
def log(function_name):
    logger.debug(f"A função {function_name} passou.")

def test_image_handler_instance(image_handler = image_handler()):
    assert image_handler.nome_com_extensão == "teste.jpg"
    assert image_handler.nome_sem_extensão == "teste"
    assert isinstance(image_handler.image, Image.Image)

def test_image_handler_remove_background(image_handler = image_handler()):
    image_before = image_handler.image.size
    image_handler.remove_background()
    assert image_before == image_handler.image.size

def test_image_handler_add_background(image_handler = image_handler()):
    color = "#fff"
    image_size_before = image_handler.image.size
    image_handler.add_background(color)
    image_size_after = image_handler.image.size

    assert image_size_after == image_size_before
    
def test_image_handler_resize_image(image_handler = image_handler()):
    image_handler = ImageHandler("C:/Users/Computador/Downloads/profile.png")
    image_before = image_handler.image.size
    image_handler.resize_image("half")
    assert image_before != image_handler.image.size
    

if __name__ == "__main__":
    funcs = [
        test_image_handler_instance,
        test_image_handler_remove_background,
        test_image_handler_add_background,
        test_image_handler_resize_image,]
    for func in funcs:
        func()
        log(func.__name__)
