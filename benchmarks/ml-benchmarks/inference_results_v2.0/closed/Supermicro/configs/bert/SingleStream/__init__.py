# Copyright (c) 2022, NVIDIA CORPORATION.  All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys
sys.path.insert(0, os.getcwd())

from code.common.constants import Benchmark, Scenario
from code.common.systems.system_list import KnownSystem
from configs.configuration import *
from configs.bert import GPUBaseConfig, CPUBaseConfig


class SingleStreamGPUBaseConfig(GPUBaseConfig):
    scenario = Scenario.SingleStream

    gpu_batch_size = 1
    gpu_copy_streams = 1
    gpu_inference_streams = 1
    use_graphs = True
    bert_opt_seqlen = 270
    use_small_tile_gemm_plugin = False


# SYS-220HE-FTNR_2_A2_TRT
@ConfigRegistry.register(HarnessType.Custom, AccuracyTarget.k_99, PowerSetting.MaxP)
class A2x2(SingleStreamGPUBaseConfig):
    system = KnownSystem.A2x2
    enable_interleaved = False
    gemm_plugin_fairshare_cache_size = 120
    single_stream_expected_latency_ns = 9000000


# SYS-220HE-FTNR_1_A2_TRT
@ConfigRegistry.register(HarnessType.Custom, AccuracyTarget.k_99, PowerSetting.MaxP)
class A2x1(SingleStreamGPUBaseConfig):
    system = KnownSystem.A2x1
    enable_interleaved = False
    gemm_plugin_fairshare_cache_size = 120
    single_stream_expected_latency_ns = 9000000

