#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (c) 2022 mundialis GmbH & Co. KG

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

Parallel ephemeral processing
"""

__license__ = "GPLv3"
__author__ = "Anika Weinmann"
__copyright__ = "Copyright 2022 mundialis GmbH & Co. KG"
__maintainer__ = "mundialis GmbH % Co. KG"


import pickle

from actinia_core.processing.actinia_processing.ephemeral_processing import \
    EphemeralProcessing

from actinia_parallel_plugin.core.batches import (
    update_and_check_batch_jobs,
)


class ParallelEphemeralProcessing(EphemeralProcessing):

    def __init__(self, rdc, batch_id, processing_block, jobid,
                 user, request_url, post_url, endpoint, method, path,
                 base_status_url):
        super(ParallelEphemeralProcessing, self).__init__(rdc)
        self.batch_id = batch_id
        self.processing_block = processing_block
        self.jobid = jobid
        self.post_url = post_url
        self.user = user
        self.request_url = request_url
        self.post_url = post_url
        self.endpoint = endpoint
        self.method = method
        self.path = path
        self.base_status_url = base_status_url

    def run(self):
        super(ParallelEphemeralProcessing, self).run()
        self._update_and_check_batch_jobs()

    def _update_and_check_batch_jobs(self):
        """Checks batch jobs and starts new batch block if the current block
        is successfully finished.
        """

        response_data = self.resource_logger.get(
            self.user_id, self.resource_id)
        _, response_model = pickle.loads(response_data)

        update_and_check_batch_jobs(
            self.resource_id,
            response_model,
            self.jobid,
            self.batch_id,
            "ephemeral",
            self.processing_block,
            self.location_name,
            None,
            self.user,
            self.request_url,
            self.post_url,
            self.endpoint,
            self.method,
            self.path,
            self.base_status_url
        )


def start_job(*args):
    processing = ParallelEphemeralProcessing(*args)
    processing.run()
