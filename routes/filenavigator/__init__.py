from __future__ import annotations

import shutil
from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import FileResponse
from pydantic import BaseModel
from starlette.concurrency import run_in_threadpool

from lib.all_configs import read_config

router = APIRouter()


# ---------- модели запросов ----------

class ReadDirIn(BaseModel):
    dir: str = "."


class WriteFileIn(BaseModel):
    dir: str
    body: str
    charset: str = "utf-8"


class ReadFileIn(BaseModel):
    dir: str
    charset: str = "utf-8"


class MkDirIn(BaseModel):
    dir: str


class DeleteIn(BaseModel):
    dir: str = "."
    name: str


class MoveIn(BaseModel):
    from_dir: str
    to_dir: str
    name: str


class RenameIn(BaseModel):
    dir: str = "."
    name: str
    new_name: str


# ---------- ответы ----------

def _ok(**kwargs) -> dict:
    return {"success": True, "error": [], **kwargs}


def _err(*messages) -> dict:
    # допускаем _err("a"), _err("a", "b"), _err(["a","b"])
    flat: list[str] = []
    for m in messages:
        if m is None:
            continue
        if isinstance(m, (list, tuple)):
            flat.extend(str(x) for x in m)
        else:
            flat.append(str(m))
    return {"success": False, "error": flat}


# ---------- безопасность путей ----------

async def _get_chroot(config: str, request: Request) -> Path:
    form = await read_config(
        request=request,
        config=config,
        script="file_navigator",
    )

    root = getattr(form, "root_directory", None)
    if not root:
        raise ValueError("root_directory не задан")

    chroot = Path(root).expanduser()

    # относительный chroot считаем от текущей рабочей директории процесса
    if not chroot.is_absolute():
        chroot = Path.cwd() / chroot

    chroot = chroot.resolve()

    if not chroot.exists() or not chroot.is_dir():
        raise ValueError("chroot не существует или не является каталогом")

    return chroot


def _safe_path(chroot: Path, rel: str | None) -> Path:
    """Возвращает путь внутри chroot или кидает ошибку."""
    rel = rel or "."
    target = (chroot / rel).resolve()

    if target != chroot and chroot not in target.parents:
        raise ValueError("путь вне chroot")

    return target


def _safe_child(chroot: Path, cur_dir: str | None, name: str) -> Path:
    """Для delete/move/rename: cur_dir + name, где name — только имя."""
    if not name:
        raise ValueError("name пустой")

    if Path(name).name != name or name in (".", ".."):
        raise ValueError("name должен быть именем, без / и ..")

    base = _safe_path(chroot, cur_dir)
    target = (base / name).resolve()

    if target != chroot and chroot not in target.parents:
        raise ValueError("путь вне chroot")

    return target


# ---------- GET: отдать root_directory ----------

@router.get("/{config}")
async def get_root(config: str, request: Request):
    form = await read_config(
        request=request,
        config=config,
        script="file_navigator",
    )
    return form.root_directory


# ---------- чтение каталога ----------

@router.post("/{config}/readir")
async def read_dir_endpoint(config: str, R: ReadDirIn, request: Request):
    try:
        chroot = await _get_chroot(config, request)
        target = _safe_path(chroot, R.dir)

        if not target.exists():
            return _err("каталог не найден")
        if not target.is_dir():
            return _err("это не каталог")

        def _list():
            items = []
            for p in target.iterdir():
                try:
                    st = p.stat()
                    size = None if p.is_dir() else st.st_size
                    mtime = int(st.st_mtime)
                except OSError:
                    size = None
                    mtime = None
                items.append({
                    "name": p.name,
                    "type": "dir" if p.is_dir() else "file",
                    "size": size,
                    "mtime": mtime,
                })
            items.sort(key=lambda x: (x["type"] != "dir", x["name"].lower()))
            return items

        items = await run_in_threadpool(_list)
        return _ok(list=items)

    except Exception as e:
        return _err(e)


# ---------- запись файла ----------

@router.post("/{config}/writefile")
async def write_file_endpoint(config: str, R: WriteFileIn, request: Request):
    try:
        chroot = await _get_chroot(config, request)
        target = _safe_path(chroot, R.dir)

        if target.exists() and target.is_dir():
            return _err("нельзя записать файл: это каталог")

        if not target.parent.exists():
            return _err("родительский каталог не существует")

        def _write():
            target.write_text(R.body, encoding=R.charset)

        try:
            await run_in_threadpool(_write)
        except UnicodeEncodeError:
            return _err(f"текст содержит символы, которые нельзя записать в кодировке {R.charset}")
        except LookupError:
            return _err(f"неизвестная кодировка {R.charset}")
        return _ok()

    except Exception as e:
        return _err(e)


# ---------- чтение файла ----------

@router.post("/{config}/readfile")
async def read_file_endpoint(config: str, R: ReadFileIn, request: Request):
    try:
        chroot = await _get_chroot(config, request)
        target = _safe_path(chroot, R.dir)

        if not target.exists():
            return _err("файл не найден")
        if not target.is_file():
            return _err("это не файл")

        def _read():
            return target.read_text(encoding=R.charset)

        try:
            body = await run_in_threadpool(_read)
        except UnicodeDecodeError:
            return _err(f"не удалось прочитать файл в кодировке {R.charset}")
        except LookupError:
            return _err(f"неизвестная кодировка {R.charset}")
        return _ok(body=body)

    except Exception as e:
        return _err(e)


# ---------- отдача сырого файла (предпросмотр/скачивание) ----------

@router.get("/{config}/raw")
async def raw_endpoint(config: str, request: Request, dir: str = ".", download: int = 0):
    try:
        chroot = await _get_chroot(config, request)
        target = _safe_path(chroot, dir)

        if not target.exists() or not target.is_file():
            return _err("файл не найден")

        return FileResponse(
            path=str(target),
            filename=target.name,
            content_disposition_type="attachment" if download else "inline",
        )

    except Exception as e:
        return _err(e)


# ---------- создание каталога ----------

@router.post("/{config}/mkdir")
async def mkdir_endpoint(config: str, R: MkDirIn, request: Request):
    try:
        chroot = await _get_chroot(config, request)
        target = _safe_path(chroot, R.dir)

        if target == chroot or target.exists():
            return _err("уже существует")

        if not target.parent.exists():
            return _err("родительский каталог не существует")

        def _mkdir():
            target.mkdir()

        await run_in_threadpool(_mkdir)
        return _ok()

    except Exception as e:
        return _err(e)


# ---------- удаление файла/каталога ----------

@router.post("/{config}/delete")
async def delete_endpoint(config: str, R: DeleteIn, request: Request):
    try:
        chroot = await _get_chroot(config, request)
        target = _safe_child(chroot, R.dir, R.name)

        if target == chroot:
            return _err("нельзя удалить корень chroot")

        if not target.exists() and not target.is_symlink():
            return _err("объект не найден")

        def _delete():
            if target.is_symlink():
                target.unlink()
            elif target.is_dir():
                shutil.rmtree(target)
            else:
                target.unlink()

        await run_in_threadpool(_delete)
        return _ok()

    except Exception as e:
        return _err(e)


# ---------- перенос файла/каталога ----------

@router.post("/{config}/move")
async def move_endpoint(config: str, R: MoveIn, request: Request):
    try:
        chroot = await _get_chroot(config, request)

        src = _safe_child(chroot, R.from_dir, R.name)
        dst_dir = _safe_path(chroot, R.to_dir)

        errors: list[str] = []

        if not src.exists() and not src.is_symlink():
            errors.append("источник не найден")

        if not dst_dir.exists() or not dst_dir.is_dir():
            errors.append("каталог назначения не найден")

        if errors:
            return _err(errors)

        dst = (dst_dir / R.name).resolve()

        if dst != chroot and chroot not in dst.parents:
            return _err("путь назначения вне chroot")

        if dst.exists() or dst.is_symlink():
            return _err("объект назначения уже существует")

        def _move():
            shutil.move(str(src), str(dst))

        await run_in_threadpool(_move)
        return _ok()

    except Exception as e:
        return _err(e)


# ---------- переименование ----------

@router.post("/{config}/rename")
async def rename_endpoint(config: str, R: RenameIn, request: Request):
    try:
        chroot = await _get_chroot(config, request)

        src = _safe_child(chroot, R.dir, R.name)
        dst = _safe_child(chroot, R.dir, R.new_name)

        errors: list[str] = []

        if not src.exists() and not src.is_symlink():
            errors.append("объект не найден")

        if dst.exists() or dst.is_symlink():
            errors.append("новое имя уже существует")

        if errors:
            return _err(errors)

        def _rename():
            src.rename(dst)

        await run_in_threadpool(_rename)
        return _ok()

    except Exception as e:
        return _err(e)