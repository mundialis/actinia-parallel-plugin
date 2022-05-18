#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (c) 2018-present mundialis GmbH & Co. KG

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

Add endpoints to flask app with endpoint definitions and routes
"""

__license__ = "GPLv3"
__author__ = "Carmen Tawalika, Anika Weinmann"
__copyright__ = "Copyright 2022 mundialis GmbH & Co. KG"
__maintainer__ = "mundialis GmbH % Co. KG"


from actinia_parallel_plugin.api.batch import BatchJobsId
from actinia_parallel_plugin.api.parallel_processing import \
    AsyncParallelPersistentResource
from actinia_parallel_plugin.core.jobtable import initJobDB, applyMigrations


# endpoints loaded if run as actinia-core plugin
def create_endpoints(flask_api):

    apidoc = flask_api

    apidoc.add_resource(
        AsyncParallelPersistentResource,
        "/locations/<string:location_name>/mapsets/"
        "<string:mapset_name>/processing_parallel")
    # apidoc.add_resource(ParallelProcessingResource, "/processing_parallel")

    # GET batch jobs by ID
    apidoc.add_resource(
        BatchJobsId,
        "/processing_parallel/batchjobs/<batchid>")
    # "/processing_parallel/jobs/<jobid>"

    # "/processing_parallel/batchjobs"
    # "/processing_parallel/jobs"



    # initilalize jobtable
    initJobDB()
    applyMigrations()
