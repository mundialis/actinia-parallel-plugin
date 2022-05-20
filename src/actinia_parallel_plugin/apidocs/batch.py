#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (c) 2021-2022 mundialis GmbH & Co. KG

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

Documentation objects for batch endpoints
"""

__license__ = "GPLv3"
__author__ = "Guido Riembauer, Anika Weinmann"
__copyright__ = "Copyright 2021-2022 mundialis GmbH & Co. KG"
__maintainer__ = "mundialis GmbH % Co. KG"


from actinia_core.models.response_models import \
    SimpleResponseModel

from actinia_parallel_plugin.model.batch import (
    BatchJobResponseModel,
)


batchjobId_get_docs = {
    "summary": "Returns batchjob by batchid.",
    "description": ("This request will get the summary for the requested "
                    "batchjob and all corresponding jobs from the jobtable."),
    "tags": [
        "processing"
    ],
    "parameters": [
      {
        "in": "path",
        "name": "batchid",
        "type": "string",
        "description": "a batchid",
        "required": True
      }
    ],
    "responses": {
        "200": {
            "description": ("The batchjob summary of the requested batchjob "
                            "and all corresponding jobs"),
            "schema": BatchJobResponseModel
        },
        "400": {
            "description": ("A short error message in case no batchid was "
                            "provided")
        },
        "404": {
            "description": ("An error message in case the batchid was "
                            "not found"),
            "schema": SimpleResponseModel
        }
    }
}
