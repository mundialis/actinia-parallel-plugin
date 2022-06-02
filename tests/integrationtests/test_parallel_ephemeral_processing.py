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

Parallel ephemeral processing tests
"""

__license__ = "GPLv3"
__author__ = "Anika Weinmann"
__copyright__ = "Copyright 2022 mundialis GmbH & Co. KG"
__maintainer__ = "mundialis GmbH % Co. KG"


import pytest

from ..test_resource_base import ActiniaResourceTestCaseBase, URL_PREFIX

PC = """{
  "jobs": [
    {
      "list": [
        {
          "module": "g.region",
          "id": "g_region_nonparallel_block1",
          "inputs":[
            {"param": "raster", "value": "elevation@PERMANENT"}
          ]
        },
        {
          "module": "r.mapcalc",
          "id": "r_mapcalc_0_nonparallel_block1",
          "inputs":[
            {"param": "expression", "value": "baum = elevation@PERMANENT * 2"}
          ]
        }
      ],
      "parallel": "false",
      "version": "1"
    },
    {
      "list": [
        {
          "module": "g.region",
          "id": "g_region_1_parallel_block2",
          "inputs":[
            {"param": "raster", "value": "elevation@PERMANENT"}
          ],
          "flags": "p"
        },
        {
          "module": "r.info",
          "id": "r_info_1_parallel_block2",
          "inputs":[
            {"param": "map", "value": "elevation@PERMANENT"}
          ]
        }
      ],
      "parallel": "true",
      "version": "1"
    },
    {
      "list": [
        {
          "module": "g.region",
          "id": "g_region_1_parallel_block2",
          "inputs":[
            {"param": "raster", "value": "elevation@PERMANENT"}
          ],
          "flags": "p"
        },
        {
          "module": "r.univar",
          "id": "r_univar_2_parallel_block2",
          "inputs":[
            {"param": "map", "value": "elevation@PERMANENT"}
          ],
          "stdout": {"id": "stats", "format": "kv", "delimiter": "="},
          "flags": "g"
        }
      ],
      "parallel": "true",
      "version": "1"
    },
    {
      "list": [
        {
          "module": "g.region",
          "id": "g_region_nonparallel_block3",
          "inputs":[
            {"param": "raster", "value": "elevation@PERMANENT"}
          ],
          "flags": "p"
        }
      ],
      "parallel": "false",
      "version": "1"
    }
  ]
}
"""


class ActiniaParallelProcessingTest(ActiniaResourceTestCaseBase):

    location = "nc_spm_08"
    base_url = f"{URL_PREFIX}/locations/{location}"
    content_type = "application/json"

    @pytest.mark.integrationtest
    def test_post_parallel_ephemeral_processing(self):
        """Test the post method of the parallel ephemeral processing endpoint
        """
        url = f"{self.base_url}/processing_parallel"

        rv = self.server.post(
            url,
            headers=self.user_auth_header,
            content_type=self.content_type,
            data=PC,
        )
        resp = self.waitAsyncBatchJob(
            rv,
            headers=self.user_auth_header,
            http_status=200,
            status="SUCCESS",
        )
        assert "actinia_core_response" in resp, \
            "No 'actinia_core_response' in response"
        assert len(resp["actinia_core_response"]) == 4, \
            "There are not 4 actinia core responses"
        process_results = [
            ac_resp["process_results"] for key, ac_resp in
            resp["actinia_core_response"].items() if
            ac_resp["process_results"] != {}]
        assert "stats" in process_results[0]
