import os

import aioredis
from fastapi import FastAPI
from fastapi_admin.app import app as admin_app
from fastapi_admin.providers.login import UsernamePasswordProvider
from starlette.staticfiles import StaticFiles
from tortoise.contrib.fastapi import register_tortoise

from .constants import BASE_DIR
from .models import Admin


def _create_app():
    app = FastAPI()
    # /admin以下に、FastAPI Adminを構築する。以下、/admin以下が管理画面。
    app.mount("/admin", admin_app)

    register_tortoise(
        app,
        config={
            # 接続する先のDBを指定
            "connections": {"default": "mysql://root@127.0.0.1:3306/fastapi_admin"},
            "apps": {
                "models": {
                    # モデル定義をパッケージレベルで指定
                    "models": ["src.models"],
                    "default_connection": "default",
                }
            },
        },
        # 起動時にスキーマも流し込む
        generate_schemas=True,
    )

    # ファイルアップロード機能を利用する場合、保存したファイルを表示するためのエンドポイントもここで作っておく。
    # アップロード画像の表示に使用
    app.mount(
        "/static",
        StaticFiles(directory=os.path.join(BASE_DIR, "static")),
        name="static",
    )

    @app.on_event("startup")
    async def startup():
        # 起動しておいたRedisへのコネクションを作成
        redis = await aioredis.from_url("redis://localhost", encoding="utf8")
        await admin_app.configure(
            logo_url="https://preview.tabler.io/static/logo-white.svg",
            # カスタムテンプレートディレクトリを指定
            template_folders=[os.path.join(BASE_DIR, "templates")],
            providers=[
                # ログイン機能の指定
                UsernamePasswordProvider(
                    # ここは任意
                    login_logo_url="https://preview.tabler.io/static/logo.svg",
                    # ログインユーザー用のモデルを指定
                    admin_model=Admin,
                )
            ],
            redis=redis,
        )

    return app


app = _create_app()
