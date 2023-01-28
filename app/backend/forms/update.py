import os
import base64
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired, FileStorage
from werkzeug.utils import secure_filename
from flask import request
from typing import Callable


class UploadAvatar(FlaskForm):
    avatar = FileField(
        "Upload",
        validators=[
            FileRequired(),
            FileAllowed(["jpg", "png"], "Images only! -> .jpg or .png"),
        ],
    )

    @staticmethod
    def _get_secure_filename(filename: str) -> str:
        return secure_filename(filename)

    @staticmethod
    def _save(file: FileStorage, filename) -> None:
        file.save(os.path.join("./tmp/avatar", filename))

    @staticmethod
    def _read_file(filename) -> bytes:
        with open(f"./tmp/avatar/{filename}", mode="rb") as file:
            return base64.b64encode(file.read())

    @staticmethod
    def _delete_file():
        if len(os.listdir("./tmp/avatar")) >= 1:

            for image in os.listdir("./tmp/avatar"):
                os.remove("{}/{}".format("./tmp/avatar", image))

    def inner(self, func: Callable) -> bool:
        file = request.files["avatar"]

        if file.filename is not None:
            filename = self._get_secure_filename(file.filename)

            self._save(file, filename)

            func(avatar=self._read_file(filename))

            # CLEAR TMP FILES
            self._delete_file()

            return True
        return False
