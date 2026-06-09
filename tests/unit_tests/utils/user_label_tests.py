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

from unittest.mock import MagicMock

from superset.utils.core import user_label


def make_user(
    first_name: str | None = None,
    last_name: str | None = None,
    username: str | None = None,
) -> MagicMock:
    user = MagicMock()
    user.first_name = first_name
    user.last_name = last_name
    user.username = username
    return user


class TestUserLabelBlackBoxEquivalencePartitioning:
    def test_valid_full_name_returns_first_last(self) -> None:
        assert user_label(make_user("Ana", "Silva", "asilva")) == "Ana Silva"

    def test_valid_only_first_name_returns_username(self) -> None:
        assert user_label(make_user("Ana", "", "asilva")) == "asilva"

    def test_valid_only_last_name_returns_username(self) -> None:
        assert user_label(make_user("", "Silva", "asilva")) == "asilva"

    def test_valid_empty_names_returns_username(self) -> None:
        assert user_label(make_user("", "", "asilva")) == "asilva"

    def test_valid_none_names_returns_username(self) -> None:
        assert user_label(make_user(None, None, "asilva")) == "asilva"

    def test_invalid_user_none_returns_none(self) -> None:
        assert user_label(None) is None

    def test_valid_names_with_internal_spaces(self) -> None:
        assert (
            user_label(make_user("Ana Paula", "da Silva", "ap"))
            == "Ana Paula da Silva"
        )

    def test_valid_last_name_whitespace_returns_concatenated(self) -> None:
        assert user_label(make_user("Ana", "   ", "asilva")) == "Ana    "

    def test_valid_first_name_whitespace_returns_concatenated(self) -> None:
        assert user_label(make_user("   ", "Silva", "asilva")) == "    Silva"

    def test_valid_both_whitespace_returns_concatenated(self) -> None:
        assert user_label(make_user("   ", "   ", "asilva")) == "       "


class TestUserLabelBlackBoxBoundaryValueAnalysis:
    def test_first_name_one_char(self) -> None:
        assert user_label(make_user("A", "Silva", "a")) == "A Silva"

    def test_last_name_one_char(self) -> None:
        assert user_label(make_user("Ana", "S", "as")) == "Ana S"

    def test_username_one_char(self) -> None:
        assert user_label(make_user("", "", "x")) == "x"

    def test_first_name_max_chars(self) -> None:
        first = "A" * 255
        assert user_label(make_user(first, "Silva", "u")) == f"{first} Silva"

    def test_last_name_max_chars(self) -> None:
        last = "B" * 255
        assert user_label(make_user("Ana", last, "u")) == f"Ana {last}"

    def test_username_max_chars(self) -> None:
        username = "c" * 255
        assert user_label(make_user("", "", username)) == username

    def test_first_name_empty_string(self) -> None:
        assert user_label(make_user("", "Silva", "u")) == "u"

    def test_last_name_empty_string(self) -> None:
        assert user_label(make_user("Ana", "", "u")) == "u"


class TestUserLabelMCDC:
    def test_condition_a_true_b_true(self) -> None:
        assert user_label(make_user("Ana", "Silva", "u")) == "Ana Silva"

    def test_condition_a_true_b_false(self) -> None:
        assert user_label(make_user("Ana", "", "u")) == "u"

    def test_condition_a_false_b_true(self) -> None:
        assert user_label(make_user("", "Silva", "u")) == "u"

    def test_condition_a_false_b_false(self) -> None:
        assert user_label(make_user("", "", "username")) == "username"

    def test_condition_a_none_b_none(self) -> None:
        assert user_label(make_user(None, None, "username")) == "username"

    def test_condition_a_none_b_truthy(self) -> None:
        assert user_label(make_user(None, "Silva", "u")) == "u"

    def test_condition_a_truthy_b_none(self) -> None:
        assert user_label(make_user("Ana", None, "u")) == "u"


class TestUserLabelWhiteBoxBranches:
    def test_user_is_none_returns_none_immediately(self) -> None:
        assert user_label(None) is None

    def test_first_and_last_truthy_returns_concatenated(self) -> None:
        assert user_label(make_user("Ana", "Silva", "u")) == "Ana Silva"

    def test_first_truthy_last_falsy_returns_username(self) -> None:
        assert user_label(make_user("Ana", "", "u")) == "u"

    def test_both_names_empty_string_returns_username(self) -> None:
        assert user_label(make_user("", "", "u")) == "u"

    def test_first_falsy_last_truthy_returns_username(self) -> None:
        assert user_label(make_user("", "Silva", "u")) == "u"

    def test_both_names_none_returns_username(self) -> None:
        assert user_label(make_user(None, None, "username")) == "username"

    def test_whitespace_bypasses_falsy_check(self) -> None:
        assert user_label(make_user("  ", "  ", "username")) == "     "


class TestUserLabelIntegration:
    def test_black_box_covers_whitespace_branch(self) -> None:
        assert user_label(make_user("  ", "  ", "username")) == "     "

    def test_white_box_guides_none_first_name_validation(self) -> None:
        assert user_label(make_user(None, "Silva", "u")) == "u"

    def test_white_box_guides_none_last_name_validation(self) -> None:
        assert user_label(make_user("Ana", None, "u")) == "u"

    def test_missing_user_none_structural_check(self) -> None:
        assert user_label(None) is None

    def test_traceability_sql_lab_query_user_label(self) -> None:
        assert user_label(make_user("Maria", "Costa", "mcosta")) == "Maria Costa"

    def test_traceability_query_history_missing_names(self) -> None:
        assert user_label(make_user("", "", "mcosta")) == "mcosta"
