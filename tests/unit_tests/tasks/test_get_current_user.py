# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
from __future__ import annotations

import importlib.util
import pathlib
import sys
import types
from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any
from unittest.mock import MagicMock, patch

import pytest
from flask import Flask

TASK_UTILS_MODULE = "superset.tasks.utils"


def _module(name: str, **attrs: Any) -> types.ModuleType:
    mod = types.ModuleType(name)
    mod.__dict__.update(attrs)
    return mod


@contextmanager
def _stubbed_imports() -> Iterator[None]:
    stubs = {
        "celery": _module("celery"),
        "celery.utils": _module("celery.utils"),
        "celery.utils.log": _module(
            "celery.utils.log",
            get_task_logger=lambda name: MagicMock(),
        ),
        "superset_core": _module("superset_core"),
        "superset_core.tasks": _module("superset_core.tasks"),
        "superset_core.tasks.types": _module(
            "superset_core.tasks.types",
            TaskProperties=dict,
            TaskScope=MagicMock(),
        ),
        "superset": _module("superset", __path__=[]),
        "superset.tasks": _module("superset.tasks", __path__=[]),
        "superset.tasks.exceptions": _module(
            "superset.tasks.exceptions",
            ExecutorNotFoundError=Exception,
            InvalidExecutorError=Exception,
        ),
        "superset.tasks.types": _module(
            "superset.tasks.types",
            ChosenExecutor=MagicMock(),
            Executor=MagicMock(),
            ExecutorType=MagicMock(),
            FixedExecutor=MagicMock(),
        ),
        "superset.utils": _module("superset.utils"),
        "superset.utils.json": _module(
            "superset.utils.json",
            loads=MagicMock(),
            dumps=MagicMock(),
            JSONDecodeError=ValueError,
        ),
        "superset.utils.hashing": _module(
            "superset.utils.hashing",
            hash_from_str=MagicMock(return_value="abc" * 30),
        ),
        "superset.utils.urls": _module(
            "superset.utils.urls",
            get_url_path=MagicMock(),
        ),
    }
    previous = {name: sys.modules.get(name) for name in stubs}

    try:
        sys.modules.update(stubs)
        yield
    finally:
        for name, previous_module in previous.items():
            if previous_module is None:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = previous_module


def _load_task_utils_module() -> types.ModuleType:
    path = pathlib.Path(__file__).parents[3] / "superset" / "tasks" / "utils.py"
    spec = importlib.util.spec_from_file_location(TASK_UTILS_MODULE, path)
    assert spec is not None
    assert spec.loader is not None
    mod = importlib.util.module_from_spec(spec)

    with _stubbed_imports():
        sys.modules[TASK_UTILS_MODULE] = mod
        spec.loader.exec_module(mod)

    return mod


task_utils = _load_task_utils_module()
get_current_user = task_utils.get_current_user


@pytest.fixture()
def app() -> Flask:
    app = Flask(__name__)
    app.config["TESTING"] = True
    return app


class TestGetCurrentUser:
    def test_returns_none_when_g_has_no_user(self, app: Flask) -> None:
        """CT01: hasattr(g, "user") is false."""
        mock_g = MagicMock(spec=[])
        with app.app_context(), patch.object(task_utils, "g", mock_g):
            assert get_current_user() is None

    def test_returns_none_when_g_user_is_none(self, app: Flask) -> None:
        """CT02: hasattr(g, "user") is true, but g.user is falsy."""
        mock_g = MagicMock()
        mock_g.user = None
        with app.app_context(), patch.object(task_utils, "g", mock_g):
            assert get_current_user() is None

    def test_returns_none_when_user_is_anonymous(self, app: Flask) -> None:
        """CT03: user exists, but user.is_anonymous is true."""
        user = MagicMock()
        user.is_anonymous = True
        mock_g = MagicMock()
        mock_g.user = user
        with app.app_context(), patch.object(task_utils, "g", mock_g):
            assert get_current_user() is None

    def test_returns_username_when_user_is_authenticated(self, app: Flask) -> None:
        """CT04: user exists and is not anonymous."""
        user = MagicMock()
        user.is_anonymous = False
        user.username = "andre"
        mock_g = MagicMock()
        mock_g.user = user
        with app.app_context(), patch.object(task_utils, "g", mock_g):
            assert get_current_user() == "andre"

    def test_returns_none_when_g_user_is_falsy_non_none(self, app: Flask) -> None:
        """CT05: g.user is falsy without being None."""
        mock_g = MagicMock()
        mock_g.user = 0
        with app.app_context(), patch.object(task_utils, "g", mock_g):
            assert get_current_user() is None

    def test_returns_empty_string_when_username_is_empty(self, app: Flask) -> None:
        """CT06: authenticated user has an empty username."""
        user = MagicMock()
        user.is_anonymous = False
        user.username = ""
        mock_g = MagicMock()
        mock_g.user = user
        with app.app_context(), patch.object(task_utils, "g", mock_g):
            assert get_current_user() == ""

    def test_returns_none_when_username_is_none(self, app: Flask) -> None:
        """CT07: authenticated user has username set to None."""
        user = MagicMock()
        user.is_anonymous = False
        user.username = None
        mock_g = MagicMock()
        mock_g.user = user
        with app.app_context(), patch.object(task_utils, "g", mock_g):
            assert get_current_user() is None
