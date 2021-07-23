# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from .. import update_dataset_access
from .. import revoke_dataset_access


def test_revoke_dataset_access(capsys, dataset_id, entity_id):

    update_dataset_access.update_dataset_access(dataset_id)
    revoke_dataset_access.revoke_dataset_access(dataset_id, entity_id)

    out, err = capsys.readouterr()
    assert f"Updated dataset '{dataset_id}' with modified user permissions." in out