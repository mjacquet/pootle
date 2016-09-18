# -*- coding: utf-8 -*-
#
# Copyright (C) Pootle contributors.
#
# This file is a part of the Pootle project. It is distributed under the GPL3
# or later license. See the LICENSE file for a copy of the license and the
# AUTHORS file for copyright and authorship information.

import pytest

from pootle.core.delegate import data_tool
from pootle_data.store_data import StoreDataTool


@pytest.mark.django_db
def test_data_tool_store(store0):
    assert data_tool.get() is None
    assert data_tool.get(store0.__class__) is StoreDataTool
    assert isinstance(store0.data_tool, StoreDataTool)
    assert store0.data_tool.context is store0


@pytest.mark.django_db
def test_data_tool_store_get_stats(store0):
    stats = store0.data_tool.get_stats()

    # TODO: remove when old stats are removed
    old_stats = store0.get_stats()

    assert (
        sorted(old_stats.keys())
        == sorted(stats.keys()))

    assert stats["translated"] == store0.data.translated_words
    assert stats["fuzzy"] == store0.data.fuzzy_words
    assert stats["total"] == store0.data.total_words
    assert stats["critical"] == store0.data.critical_checks
    assert stats["suggestions"] == store0.data.pending_suggestions
    assert stats["children"] == {}
    assert stats["is_dirty"] is False
    # this is the actually last updated unit - called "lastaction"
    last_submission_info = (
        store0.data.last_submission.get_submission_info())
    assert (
        sorted(stats["lastaction"].items())
        == sorted(last_submission_info.items()))
    # apparently "updated" means created
    last_updated_info = (
        store0.data.last_created_unit.get_last_updated_info())
    assert (
        sorted(stats["lastupdated"].items())
        == sorted(last_updated_info.items()))
