import pytest

from src.functions import allowed_file


@pytest.mark.parametrize(
    "filename, expected",
    [
        ("document.pdf", True),
        ("image.jpeg", True),
        ("archive.zip", False),
        ("file_without_extension", False),
        (".hiddenfile", False),
        ("file.TIFF", False),
        ("script.js", False),
    ],
)
async def test_allowed_file(filename, expected):
    """
    Проверяет, разрешен ли файл для загрузки, в зависимости от его расширения.
    """
    assert await allowed_file(filename) == expected
