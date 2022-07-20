import os

from fastapi_admin.app import app
from fastapi_admin.file_upload import FileUpload
from fastapi_admin.resources import (
    Action,
    Dropdown,
    Field,
    Link,
    Model,
    ToolbarAction,
    displays,
    inputs,
)

from .constants import BASE_DIR
from .models import Admin

upload = FileUpload(uploads_dir=os.path.join(BASE_DIR, "static", "uploads"))


@app.register
class Dashboard(Link):
    label = "Dashboard"
    icon = "fas fa-home"
    url = "/admin"


@app.register
class GitHub(Link):
    label = "GitHub"
    icon = "fab fa-github"
    url = "https://github.com/soymsk/"
    target = "_blank"


@app.register
class AdminResource(Model):
    label = "Admin"
    # 管理するTortoise ORMモデルを指定
    model = Admin
    icon = "fas fa-user"
    fields = [
        "id",
        "username",
        Field(
            name="password",
            label="Password",
            display=displays.InputOnly(),  # リストに表示しない
            input_=inputs.Password(),  # HTML form input typeをpasswordに指定
        ),
        Field(
            name="email",
            label="Email",
            input_=inputs.Email(),  # HTML form input typeをemailに指定
        ),
        Field(
            name="avatar",
            label="Avatar",
            display=displays.Image(width="40"),
            input_=inputs.Image(null=True, upload=upload),
        ),
        "created_at",
    ]
