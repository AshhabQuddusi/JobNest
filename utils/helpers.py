"""
General helper utilities.
"""

import os
import uuid
from werkzeug.utils import secure_filename
from config import Config


def allowed_file(filename: str) -> bool:
    """Check that a filename has an allowed extension."""
    return (
        '.' in filename
        and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS
    )


def save_uploaded_file(file_storage) -> str:
    """
    Save a Werkzeug FileStorage object to the upload folder.
    Returns the unique filename used on disk.
    Raises ValueError for invalid files.
    """
    if not file_storage or file_storage.filename == '':
        raise ValueError("No file selected.")

    if not allowed_file(file_storage.filename):
        raise ValueError("Only PDF files are accepted.")

    original_name = secure_filename(file_storage.filename)
    # Prefix with UUID to avoid name collisions
    unique_name = f"{uuid.uuid4().hex}_{original_name}"

    os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
    save_path = os.path.join(Config.UPLOAD_FOLDER, unique_name)
    file_storage.save(save_path)

    return unique_name


def delete_file_if_exists(filename: str) -> None:
    """Remove a file from the upload folder silently."""
    if not filename:
        return
    path = os.path.join(Config.UPLOAD_FOLDER, filename)
    try:
        if os.path.isfile(path):
            os.remove(path)
    except OSError:
        pass


def get_upload_path(filename: str) -> str:
    """Return the absolute path for a stored upload filename."""
    return os.path.join(Config.UPLOAD_FOLDER, filename)
