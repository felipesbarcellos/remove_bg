from util.ImageHandler import ImageHandler
from util.constants import TEST_FILE, PATH_INPUT, PATH_OUTPUT
from loguru import logger
from PIL import Image
import pytest
import os


def image_handler() -> ImageHandler:
    input_path = f"{PATH_INPUT}{TEST_FILE}"
    return ImageHandler(input_path)


def log(function_name):
    logger.debug(f"A função {function_name} passou.")


def test_image_handler_instance(image_handler=image_handler()):
    assert image_handler.nome_com_extensão == "teste.jpg"
    assert image_handler.nome_sem_extensão == "teste"
    assert isinstance(image_handler.image, Image.Image)


def test_image_handler_remove_background(image_handler=image_handler()):
    image_before = image_handler.image.size
    image_handler.remove_background()
    assert image_before == image_handler.image.size


def test_image_handler_add_background(image_handler=image_handler()):
    color = "#fff"
    image_size_before = image_handler.image.size
    image_handler.add_background(color)
    image_size_after = image_handler.image.size
    assert image_size_after == image_size_before


def test_image_handler_resize_image(image_handler=image_handler()):
    # Use the same test image as other tests to avoid FileNotFoundError
    image_before = image_handler.image.size
    image_handler.resize_image("half")
    assert image_before != image_handler.image.size


def test_image_handler_save(tmp_path):
    handler = image_handler()
    save_path = handler.output_path
    # Ensure save is called with the correct argument (the path as string)
    handler.save()
    assert os.path.exists(save_path)
    img = Image.open(save_path)
    assert isinstance(img, Image.Image)


def test_image_handler_get_image_format(image_handler=image_handler()):
    assert image_handler.image.format in ["JPEG", "JPG", "PNG", None]


def test_image_handler_invalid_file():
    with pytest.raises(Exception):
        ImageHandler("invalid_path/nonexistent.jpg")


def test_image_handler_add_background_invalid_color(image_handler=image_handler()):
    with pytest.raises(ValueError):
        image_handler.add_background("notacolor")


def test_image_handler_resize_invalid_mode(image_handler=image_handler()):
    # Pass an invalid mode string to trigger ValueError, not a wrong type
    with pytest.raises(ValueError):
        image_handler.resize_image("invalid_mode")


if __name__ == "__main__":
    funcs = [
        test_image_handler_instance,
        test_image_handler_remove_background,
        test_image_handler_add_background,
        test_image_handler_resize_image,
        test_image_handler_save,
        test_image_handler_get_image_format,
        test_image_handler_invalid_file,
        test_image_handler_add_background_invalid_color,
        test_image_handler_resize_invalid_mode,
    ]
    for func in funcs:
        try:
            func()
            log(func.__name__)
        except Exception as e:
            logger.error(f"Erro na função {func.__name__}: {e}")
    assert isinstance(image_handler.image, Image.Image)
