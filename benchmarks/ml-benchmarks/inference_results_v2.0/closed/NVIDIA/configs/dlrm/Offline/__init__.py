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

from importlib import import_module
from code.common.constants import Benchmark, Scenario
from code.common.systems.system_list import KnownSystem
from configs.configuration import *

ParentConfig = import_module("configs.dlrm")
GPUBaseConfig = ParentConfig.GPUBaseConfig


class OfflineGPUBaseConfig(GPUBaseConfig):
    scenario = Scenario.Offline
    check_contiguity = True
    use_small_tile_gemm_plugin = True


@ConfigRegistry.register(HarnessType.Custom, AccuracyTarget.k_99, PowerSetting.MaxP)
class A100_PCIe_80GBx1(OfflineGPUBaseConfig):
    system = KnownSystem.A100_PCIe_80GBx1
    complete_threads = 1
    deque_timeout_usec = 1
    gemm_plugin_fairshare_cache_size = 18
    gpu_batch_size = 315000
    offline_expected_qps = 270000
    max_pairs_per_staging_thread = 262100
    num_staging_batches = 8
    num_staging_threads = 8
    use_jemalloc = True


@ConfigRegistry.register(HarnessType.Custom, AccuracyTarget.k_99_9, PowerSetting.MaxP)
class A100_PCIe_80GBx1_HighAccuracy(A100_PCIe_80GBx1):
    pass


@ConfigRegistry.register(HarnessType.Triton, AccuracyTarget.k_99, PowerSetting.MaxP)
class A100_PCIe_80GBx1_Triton(A100_PCIe_80GBx1):
    batch_triton_requests = True
    buffer_manager_thread_count = 8
    use_triton = True


@ConfigRegistry.register(HarnessType.Triton, AccuracyTarget.k_99_9, PowerSetting.MaxP)
class A100_PCIe_80GBx1_HighAccuracy_Triton(A100_PCIe_80GBx1_Triton):
    pass


@ConfigRegistry.register(HarnessType.Custom, AccuracyTarget.k_99, PowerSetting.MaxP)
class A100_PCIe_80GBx8(A100_PCIe_80GBx1):
    system = KnownSystem.A100_PCIe_80GBx8
    offline_expected_qps = 2280000
    numa_config = "3:0-15&2:16-31&1:32-47&0:48-63&7:64-79&6:80-95&5:96-111&4:112-127"


@ConfigRegistry.register(HarnessType.Custom, AccuracyTarget.k_99_9, PowerSetting.MaxP)
class A100_PCIe_80GBx8_HighAccuracy(A100_PCIe_80GBx8):
    pass


@ConfigRegistry.register(HarnessType.Triton, AccuracyTarget.k_99, PowerSetting.MaxP)
class A100_PCIe_80GBx8_Triton(A100_PCIe_80GBx8):
    offline_expected_qps = 1896400
    batch_triton_requests = True
    buffer_manager_thread_count = 0
    use_triton = True
    gather_kernel_buffer_threshold = 64
    num_concurrent_batchers = 1


@ConfigRegistry.register(HarnessType.Triton, AccuracyTarget.k_99_9, PowerSetting.MaxP)
class A100_PCIe_80GBx8_HighAccuracy_Triton(A100_PCIe_80GBx8_Triton):
    pass


@ConfigRegistry.register(HarnessType.Custom, AccuracyTarget.k_99, PowerSetting.MaxQ)
class A100_PCIe_80GBx8_MaxQ(A100_PCIe_80GBx8):
    offline_expected_qps = 1690000
    use_jemalloc = False
    numa_config = "3:0-7&2:8-15&1:16-23&0:24-31&7:32-39&6:40-47&5:48-55&4:56-63"
    power_limit = 225


@ConfigRegistry.register(HarnessType.Custom, AccuracyTarget.k_99_9, PowerSetting.MaxQ)
class A100_PCIe_80GBx8_HighAccuracy_MaxQ(A100_PCIe_80GBx8_MaxQ):
    gpu_batch_size = 262100


@ConfigRegistry.register(HarnessType.Triton, AccuracyTarget.k_99, PowerSetting.MaxQ)
class A100_PCIe_80GBx8_Triton_MaxQ(A100_PCIe_80GBx8_MaxQ):
    offline_expected_qps = 280000
    use_jemalloc = True
    batch_triton_requests = True
    buffer_manager_thread_count = 8
    use_triton = True


@ConfigRegistry.register(HarnessType.Triton, AccuracyTarget.k_99_9, PowerSetting.MaxQ)
class A100_PCIe_80GBx8_HighAccuracy_Triton_MaxQ(A100_PCIe_80GBx8_Triton_MaxQ):
    pass


@ConfigRegistry.register(HarnessType.Custom, AccuracyTarget.k_99, PowerSetting.MaxP)
class A100_PCIe_80GB_aarch64x1(OfflineGPUBaseConfig):
    system = KnownSystem.A100_PCIe_80GB_ARMx1
    complete_threads = 1
    deque_timeout_usec = 1
    gemm_plugin_fairshare_cache_size = 18
    gpu_batch_size = 315000
    offline_expected_qps = 270000
    max_pairs_per_staging_thread = 262100
    num_staging_batches = 8
    num_staging_threads = 8
    use_jemalloc = True


@ConfigRegistry.register(HarnessType.Triton, AccuracyTarget.k_99, PowerSetting.MaxP)
class A100_PCIe_80GB_aarch64x1_Triton(A100_PCIe_80GB_aarch64x1):
    batch_triton_requests = True
    buffer_manager_thread_count = 8
    use_triton = True


@ConfigRegistry.register(HarnessType.Custom, AccuracyTarget.k_99_9, PowerSetting.MaxP)
class A100_PCIe_80GB_aarch64x1_HighAccuracy(A100_PCIe_80GB_aarch64x1):
    pass


@ConfigRegistry.register(HarnessType.Triton, AccuracyTarget.k_99_9, PowerSetting.MaxP)
class A100_PCIe_80GB_aarch64x1_HighAccuracy_Triton(A100_PCIe_80GB_aarch64x1_Triton):
    pass


@ConfigRegistry.register(HarnessType.Custom, AccuracyTarget.k_99, PowerSetting.MaxP)
class A100_PCIe_80GB_aarch64x2(A100_PCIe_80GB_aarch64x1):
    system = KnownSystem.A100_PCIe_80GB_ARMx2
    offline_expected_qps = 560000
    # TODO: set numa
    numa_config = None


@ConfigRegistry.register(HarnessType.Triton, AccuracyTarget.k_99, PowerSetting.MaxP)
class A100_PCIe_80GB_aarch64x2_Triton(A100_PCIe_80GB_aarch64x2):
    use_triton = True
    batch_triton_requests = True


@ConfigRegistry.register(HarnessType.Custom, AccuracyTarget.k_99_9, PowerSetting.MaxP)
class A100_PCIe_80GB_aarch64x2_HighAccuracy(A100_PCIe_80GB_aarch64x2):
    pass


@ConfigRegistry.register(HarnessType.Triton, AccuracyTarget.k_99_9, PowerSetting.MaxP)
class A100_PCIe_80GB_aarch64x2_HighAccuracy_Triton(A100_PCIe_80GB_aarch64x2_Triton):
    pass


@ConfigRegistry.register(HarnessType.Custom, AccuracyTarget.k_99, PowerSetting.MaxP)
class A100_PCIe_80GB_aarch64x4(A100_PCIe_80GB_aarch64x1):
    system = KnownSystem.A100_PCIe_80GB_ARMx4
    offline_expected_qps = 1100000
    # TODO: set numa
    numa_config = None


@ConfigRegistry.register(HarnessType.Triton, AccuracyTarget.k_99, PowerSetting.MaxP)
class A100_PCIe_80GB_aarch64x4_Triton(A100_PCIe_80GB_aarch64x4):
    use_triton = True
    batch_triton_requests = True
    num_concurrent_batchers = 1


@ConfigRegistry.register(HarnessType.Custom, AccuracyTarget.k_99_9, PowerSetting.MaxP)
class A100_PCIe_80GB_aarch64x4_HighAccuracy(A100_PCIe_80GB_aarch64x4):
    pass


@ConfigRegistry.register(HarnessType.Triton, AccuracyTarget.k_99_9, PowerSetting.MaxP)
class A100_PCIe_80GB_aarch64x4_HighAccuracy_Triton(A100_PCIe_80GB_aarch64x4_Triton):
    pass


@ConfigRegistry.register(HarnessType.Custom, AccuracyTarget.k_99, PowerSetting.MaxQ)
class A100_PCIe_80GB_aarch64x4_MaxQ(A100_PCIe_80GB_aarch64x4):
    offline_expected_qps = 960000
    use_jemalloc = False
    # TODO: set numa
    numa_config = None
    power_limit = 225


@ConfigRegistry.register(HarnessType.Custom, AccuracyTarget.k_99_9, PowerSetting.MaxQ)
class A100_PCIe_80GB_aarch64x4_HighAccuracy_MaxQ(A100_PCIe_80GB_aarch64x4_MaxQ):
    pass


@ConfigRegistry.register(HarnessType.Custom, AccuracyTarget.k_99, PowerSetting.MaxP)
class A100_PCIe_aarch64x1(OfflineGPUBaseConfig):
    system = KnownSystem.A100_PCIe_40GB_ARMx1
    complete_threads = 1
    deque_timeout_usec = 1
    gemm_plugin_fairshare_cache_size = 18
    gpu_batch_size = 315000
    offline_expected_qps = 270000
    max_pairs_per_staging_thread = 262100
    num_staging_batches = 8
    num_staging_threads = 8
    use_jemalloc = True


@ConfigRegistry.register(HarnessType.Triton, AccuracyTarget.k_99, PowerSetting.MaxP)
class A100_PCIe_aarch64x1_Triton(A100_PCIe_aarch64x1):
    use_triton = True
    batch_triton_requests = True


@ConfigRegistry.register(HarnessType.Custom, AccuracyTarget.k_99_9, PowerSetting.MaxP)
class A100_PCIe_aarch64x1_HighAccuracy(A100_PCIe_aarch64x1):
    pass


@ConfigRegistry.register(HarnessType.Triton, AccuracyTarget.k_99_9, PowerSetting.MaxP)
class A100_PCIe_aarch64x1_HighAccuracy_Triton(A100_PCIe_aarch64x1_Triton):
    pass


@ConfigRegistry.register(HarnessType.Custom, AccuracyTarget.k_99, PowerSetting.MaxP)
class A100_PCIe_aarch64x2(A100_PCIe_aarch64x1):
    system = KnownSystem.A100_PCIe_40GB_ARMx2
    offline_expected_qps = 560000
    # TODO: set numa
    numa_config = None


@ConfigRegistry.register(HarnessType.Triton, AccuracyTarget.k_99, PowerSetting.MaxP)
class A100_PCIe_aarch64x2_Triton(A100_PCIe_aarch64x2):
    use_triton = True
    batch_triton_requests = True
    num_concurrent_batchers = 1


@ConfigRegistry.register(HarnessType.Custom, AccuracyTarget.k_99_9, PowerSetting.MaxP)
class A100_PCIe_aarch64x2_HighAccuracy(A100_PCIe_aarch64x2):
    pass


@ConfigRegistry.register(HarnessType.Triton, AccuracyTarget.k_99_9, PowerSetting.MaxP)
class A100_PCIe_aarch64x2_HighAccuracy_Triton(A100_PCIe_aarch64x2_Triton):
    pass


@ConfigRegistry.register(HarnessType.Custom, AccuracyTarget.k_99, PowerSetting.MaxP)
class A100_PCIe_aarch64x4(A100_PCIe_aarch64x1):
    system = KnownSystem.A100_PCIe_40GB_ARMx4
    offline_expected_qps = 1100000
    # TODO: set numa
    numa_config = None


@ConfigRegistry.register(HarnessType.Triton, AccuracyTarget.k_99, PowerSetting.MaxP)
class A100_PCIe_aarch64x4_Triton(A100_PCIe_aarch64x4):
    batch_triton_requests = True
    use_triton = True
    num_concurrent_batchers = 1


@ConfigRegistry.register(HarnessType.Custom, AccuracyTarget.k_99_9, PowerSetting.MaxP)
class A100_PCIe_aarch64x4_HighAccuracy(A100_PCIe_aarch64x4):
    pass


@ConfigRegistry.register(HarnessType.Triton, AccuracyTarget.k_99_9, PowerSetting.MaxP)
class A100_PCIe_aarch64x4_HighAccuracy_Triton(A100_PCIe_aarch64x4_Triton):
    pass


@ConfigRegistry.register(HarnessType.Custom, AccuracyTarget.k_99, PowerSetting.MaxQ)
class A100_PCIe_aarch64x4_MaxQ(A100_PCIe_aarch64x4):
    offline_expected_qps = 800000
    use_jemalloc = False
    # TODO: set numa
    numa_config = None
    power_limit = 225


@ConfigRegistry.register(HarnessType.Custom, AccuracyTarget.k_99_9, PowerSetting.MaxQ)
class A100_PCIe_aarch64x4_HighAccuracy_MaxQ(A100_PCIe_aarch64x4_MaxQ):
    pass


@ConfigRegistry.register(HarnessType.Custom, AccuracyTarget.k_99, PowerSetting.MaxP)
class DRIVE_A100_PCIE(OfflineGPUBaseConfig):
    system = KnownSystem.DRIVE_A100_PCIE
    complete_threads = 1
    deque_timeout_usec = 1
    gemm_plugin_fairshare_cache_size = 18
    gpu_batch_size = 315000
    offline_expected_qps = 270000
    max_pairs_per_staging_thread = 262100
    num_staging_batches = 8
    num_staging_threads = 8
    use_jemalloc = True


@ConfigRegistry.register(HarnessType.Custom, AccuracyTarget.k_99_9, PowerSetting.MaxP)
class DRIVE_A100_PCIE_HighAccuracy(DRIVE_A100_PCIE):
    pass


@ConfigRegistry.register(HarnessType.Triton, AccuracyTarget.k_99, PowerSetting.MaxP)
class DRIVE_A100_PCIE_Triton(DRIVE_A100_PCIE):
    batch_triton_requests = True
    buffer_manager_thread_count = 8
    use_triton = True


@ConfigRegistry.register(HarnessType.Triton, AccuracyTarget.k_99_9, PowerSetting.MaxP)
class DRIVE_A100_PCIE_HighAccuracy_Triton(DRIVE_A100_PCIE_Triton):
    pass


@ConfigRegistry.register(HarnessType.Custom, AccuracyTarget.k_99, PowerSetting.MaxP)
class A100_PCIe_MIG_1x1g5gb(OfflineGPUBaseConfig):
    system = KnownSystem.A100_PCIe_40GB_MIG_1x1g_5gb
    complete_threads = 2
    deque_timeout_usec = 1
    embedding_weights_on_gpu_part = 0.3
    gemm_plugin_fairshare_cache_size = 18
    gpu_batch_size = 51200
    offline_expected_qps = 36000
    max_pairs_per_staging_thread = 51200
    num_staging_batches = 4
    num_staging_threads = 4
    use_jemalloc = True


@ConfigRegistry.register(HarnessType.Custom, AccuracyTarget.k_99_9, PowerSetting.MaxP)
class A100_PCIe_MIG_1x1g5gb_HighAccuracy(A100_PCIe_MIG_1x1g5gb):
    pass


@ConfigRegistry.register(HarnessType.Triton, AccuracyTarget.k_99, PowerSetting.MaxP)
class A100_PCIe_MIG_1x1g5gb_Triton(A100_PCIe_MIG_1x1g5gb):
    batch_triton_requests = True
    buffer_manager_thread_count = 8
    use_triton = True
    num_concurrent_batchers = 1


@ConfigRegistry.register(HarnessType.Triton, AccuracyTarget.k_99_9, PowerSetting.MaxP)
class A100_PCIe_MIG_1x1g5gb_HighAccuracy_Triton(A100_PCIe_MIG_1x1g5gb):
    buffer_manager_thread_count = 8
    use_triton = True


@ConfigRegistry.register(HarnessType.Custom, AccuracyTarget.k_99, PowerSetting.MaxP)
class A100_PCIe_80GB_MIG_1x1g10gb(OfflineGPUBaseConfig):
    system = KnownSystem.A100_PCIe_80GB_MIG_1x1g_10gb
    complete_threads = 2
    deque_timeout_usec = 1
    embedding_weights_on_gpu_part = 0.3
    gemm_plugin_fairshare_cache_size = 18
    gpu_batch_size = 51200
    offline_expected_qps = 40000
    max_pairs_per_staging_thread = 51200
    num_staging_batches = 4
    num_staging_threads = 4
    use_jemalloc = True


@ConfigRegistry.register(HarnessType.HeteroMIG, AccuracyTarget.k_99, PowerSetting.MaxP)
class A100_PCIe_80GB_MIG_1x1g10gb_Hetero(A100_PCIe_80GB_MIG_1x1g10gb):
    offline_expected_qps = 36000


@ConfigRegistry.register(HarnessType.Custom, AccuracyTarget.k_99_9, PowerSetting.MaxP)
class A100_PCIe_80GB_MIG_1x1g10gb_HighAccuracy(A100_PCIe_80GB_MIG_1x1g10gb):
    pass


@ConfigRegistry.register(HarnessType.HeteroMIG, AccuracyTarget.k_99_9, PowerSetting.MaxP)
class A100_PCIe_80GB_MIG_1x1g10gb_Hetero_HighAccuracy(A100_PCIe_80GB_MIG_1x1g10gb_HighAccuracy):
    offline_expected_qps = 36000


@ConfigRegistry.register(HarnessType.Triton, AccuracyTarget.k_99, PowerSetting.MaxP)
class A100_PCIe_80GB_MIG_1x1g10gb_Triton(A100_PCIe_80GB_MIG_1x1g10gb):
    batch_triton_requests = True
    buffer_manager_thread_count = 8
    use_triton = True


@ConfigRegistry.register(HarnessType.Triton, AccuracyTarget.k_99_9, PowerSetting.MaxP)
class A100_PCIe_80GB_MIG_1x1g10gb_HighAccuracy_Triton(A100_PCIe_80GB_MIG_1x1g10gb_Triton):
    pass


@ConfigRegistry.register(HarnessType.Triton, AccuracyTarget.k_99, PowerSetting.MaxP)
class A100_PCIe_80GB_MIG_56x1g10gb_Triton(A100_PCIe_80GB_MIG_1x1g10gb):
    system = KnownSystem.A100_PCIe_80GB_MIG_56x1g_10gb
    offline_expected_qps = 2240000
    batch_triton_requests = True
    buffer_manager_thread_count = 8
    use_triton = True


@ConfigRegistry.register(HarnessType.Triton, AccuracyTarget.k_99_9, PowerSetting.MaxP)
class A100_PCIe_80GB_MIG_56x1g10gb_HighAccuracy_Triton(A100_PCIe_80GB_MIG_56x1g10gb_Triton):
    pass


@ConfigRegistry.register(HarnessType.Custom, AccuracyTarget.k_99, PowerSetting.MaxP)
class A100_PCIex1(OfflineGPUBaseConfig):
    system = KnownSystem.A100_PCIe_40GBx1
    complete_threads = 1
    deque_timeout_usec = 1
    gemm_plugin_fairshare_cache_size = 18
    gpu_batch_size = 315000
    offline_expected_qps = 270000
    max_pairs_per_staging_thread = 262100
    num_staging_batches = 8
    num_staging_threads = 8
    use_jemalloc = True


@ConfigRegistry.register(HarnessType.Custom, AccuracyTarget.k_99_9, PowerSetting.MaxP)
class A100_PCIex1_HighAccuracy(A100_PCIex1):
    pass


@ConfigRegistry.register(HarnessType.Triton, AccuracyTarget.k_99, PowerSetting.MaxP)
class A100_PCIex1_Triton(A100_PCIex1):
    batch_triton_requests = True
    buffer_manager_thread_count = 8
    use_triton = True


@ConfigRegistry.register(HarnessType.Triton, AccuracyTarget.k_99_9, PowerSetting.MaxP)
class A100_PCIex1_HighAccuracy_Triton(A100_PCIex1_Triton):
    pass


@ConfigRegistry.register(HarnessType.Custom, AccuracyTarget.k_99, PowerSetting.MaxP)
class A100_PCIex8(A100_PCIex1):
    system = KnownSystem.A100_PCIe_40GBx8
    offline_expected_qps = 2160000
    numa_config = "3:0-15&2:16-31&1:32-47&0:48-63&7:64-79&6:80-95&5:96-111&4:112-127"


@ConfigRegistry.register(HarnessType.Custom, AccuracyTarget.k_99_9, PowerSetting.MaxP)
class A100_PCIex8_HighAccuracy(A100_PCIex8):
    pass


@ConfigRegistry.register(HarnessType.Triton, AccuracyTarget.k_99, PowerSetting.MaxP)
class A100_PCIex8_Triton(A100_PCIex8):
    offline_expected_qps = 1600000
    batch_triton_requests = True
    buffer_manager_thread_count = 0
    use_triton = True
    gather_kernel_buffer_threshold = 64
    num_concurrent_batchers = 1


@ConfigRegistry.register(HarnessType.Triton, AccuracyTarget.k_99_9, PowerSetting.MaxP)
class A100_PCIex8_HighAccuracy_Triton(A100_PCIex8_Triton):
    pass


@ConfigRegistry.register(HarnessType.Custom, AccuracyTarget.k_99, PowerSetting.MaxQ)
class A100_PCIex8_MaxQ(A100_PCIex8):
    offline_expected_qps = 1890000
    use_jemalloc = False
    numa_config = "3:0-7&2:8-15&1:16-23&0:24-31&7:32-39&6:40-47&5:48-55&4:56-63"
    power_limit = 225


@ConfigRegistry.register(HarnessType.Custom, AccuracyTarget.k_99_9, PowerSetting.MaxQ)
class A100_PCIex8_HighAccuracy_MaxQ(A100_PCIex8_MaxQ):
    gpu_batch_size = 262100


@ConfigRegistry.register(HarnessType.Triton, AccuracyTarget.k_99, PowerSetting.MaxQ)
class A100_PCIex8_Triton_MaxQ(A100_PCIex8_MaxQ):
    system = KnownSystem.A100_PCIe_40GBx8
    offline_expected_qps = 280000
    use_jemalloc = True
    batch_triton_requests = True
    buffer_manager_thread_count = 8
    power_limit = 225
    use_triton = True
    num_concurrent_batchers = 1


@ConfigRegistry.register(HarnessType.Triton, AccuracyTarget.k_99_9, PowerSetting.MaxQ)
class A100_PCIex8_HighAccuracy_Triton_MaxQ(A100_PCIex8_Triton_MaxQ):
    pass


@ConfigRegistry.register(HarnessType.Custom, AccuracyTarget.k_99, PowerSetting.MaxP)
class A100_SXM_80GB_MIG_1x1g10gb(OfflineGPUBaseConfig):
    system = KnownSystem.A100_SXM_80GB_MIG_1x1g_10gb
    complete_threads = 2
    deque_timeout_usec = 1
    embedding_weights_on_gpu_part = 0.3
    gemm_plugin_fairshare_cache_size = 18
    gpu_batch_size = 51200
    offline_expected_qps = 40000
    max_pairs_per_staging_thread = 51200
    num_staging_batches = 4
    num_staging_threads = 4
    use_jemalloc = True


@ConfigRegistry.register(HarnessType.HeteroMIG, AccuracyTarget.k_99, PowerSetting.MaxP)
class A100_SXM_80GB_MIG_1x1g10gb_Hetero(A100_SXM_80GB_MIG_1x1g10gb):
    pass


@ConfigRegistry.register(HarnessType.Custom, AccuracyTarget.k_99_9, PowerSetting.MaxP)
class A100_SXM_80GB_MIG_1x1g10gb_HighAccuracy(A100_SXM_80GB_MIG_1x1g10gb):
    pass


@ConfigRegistry.register(HarnessType.HeteroMIG, AccuracyTarget.k_99_9, PowerSetting.MaxP)
class A100_SXM_80GB_MIG_1x1g10gb_Hetero_HighAccuracy(A100_SXM_80GB_MIG_1x1g10gb_HighAccuracy):
    pass


@ConfigRegistry.register(HarnessType.Triton, AccuracyTarget.k_99, PowerSetting.MaxP)
class A100_SXM_80GB_MIG_1x1g10gb_Triton(A100_SXM_80GB_MIG_1x1g10gb):
    batch_triton_requests = True
    buffer_manager_thread_count = 8
    use_triton = True


@ConfigRegistry.register(HarnessType.Triton, AccuracyTarget.k_99_9, PowerSetting.MaxP)
class A100_SXM_80GB_MIG_1x1g10gb_HighAccuracy_Triton(A100_SXM_80GB_MIG_1x1g10gb_Triton):
    pass


@ConfigRegistry.register(HarnessType.Triton, AccuracyTarget.k_99, PowerSetting.MaxP)
class A100_SXM_80GB_MIG_56x1g10gb_Triton(A100_SXM_80GB_MIG_1x1g10gb):
    system = KnownSystem.A100_SXM_80GB_MIG_56x1g_10gb
    offline_expected_qps = 2240000
    batch_triton_requests = True
    buffer_manager_thread_count = 8
    use_triton = True


@ConfigRegistry.register(HarnessType.Triton, AccuracyTarget.k_99_9, PowerSetting.MaxP)
class A100_SXM_80GB_MIG_56x1g10gb_HighAccuracy_Triton(A100_SXM_80GB_MIG_56x1g10gb_Triton):
    pass


@ConfigRegistry.register(HarnessType.Custom, AccuracyTarget.k_99, PowerSetting.MaxP)
class A100_SXM_80GBx1(OfflineGPUBaseConfig):
    system = KnownSystem.A100_SXM_80GBx1
    complete_threads = 1
    deque_timeout_usec = 1
    gemm_plugin_fairshare_cache_size = 18
    gpu_batch_size = 262100
    offline_expected_qps = 310000
    max_pairs_per_staging_thread = 262100
    num_staging_batches = 8
    num_staging_threads = 8
    start_from_device = True
    use_jemalloc = True


@ConfigRegistry.register(HarnessType.Custom, AccuracyTarget.k_99_9, PowerSetting.MaxP)
class A100_SXM_80GBx1_HighAccuracy(A100_SXM_80GBx1):
    pass


@ConfigRegistry.register(HarnessType.Triton, AccuracyTarget.k_99_9, PowerSetting.MaxP)
class A100_SXM_80GBx1_HighAccuracy_Triton(A100_SXM_80GBx1):
    batch_triton_requests = True
    buffer_manager_thread_count = 0
    gather_kernel_buffer_threshold = 2
    use_triton = True


@ConfigRegistry.register(HarnessType.Triton, AccuracyTarget.k_99, PowerSetting.MaxP)
class A100_SXM_80GBx1_Triton(A100_SXM_80GBx1):
    batch_triton_requests = True
    buffer_manager_thread_count = 0
    gather_kernel_buffer_threshold = 2
    use_triton = True


@ConfigRegistry.register(HarnessType.Custom, AccuracyTarget.k_99, PowerSetting.MaxP)
class A100_SXM_80GBx4(OfflineGPUBaseConfig):
    _system_alias = "DGX Station A100 - Red October"
    _notes = "This should not inherit from A100_SXM_80GB (DGX-A100), and cannot use start_from_device"

    system = KnownSystem.A100_SXM_80GB_ROx4
    complete_threads = 1
    deque_timeout_usec = 1
    gemm_plugin_fairshare_cache_size = 18
    gpu_batch_size = 334000
    offline_expected_qps = 1000000
    max_pairs_per_staging_thread = 262100
    num_staging_batches = 8
    num_staging_threads = 8
    use_jemalloc = True
    numa_config = "3:0-15,64-79&2:16-31,80-95&1:32-47,96-111&0:48-63,112-127"


@ConfigRegistry.register(HarnessType.Custom, AccuracyTarget.k_99_9, PowerSetting.MaxP)
class A100_SXM_80GBx4_HighAccuracy(A100_SXM_80GBx4):
    pass


@ConfigRegistry.register(HarnessType.Triton, AccuracyTarget.k_99, PowerSetting.MaxP)
class A100_SXM_80GBx4_Triton(A100_SXM_80GBx4):
    _system_alias = "DGX Station A100 - Red October"
    _notes = "This should not inherit from A100_SXM_80GB (DGX-A100), and cannot use start_from_device"

    gpu_batch_size = 262100
    batch_triton_requests = True
    buffer_manager_thread_count = 0
    gather_kernel_buffer_threshold = 32
    use_triton = True
    num_concurrent_batchers = 1


@ConfigRegistry.register(HarnessType.Triton, AccuracyTarget.k_99_9, PowerSetting.MaxP)
class A100_SXM_80GBx4_HighAccuracy_Triton(A100_SXM_80GBx4_Triton):
    gpu_batch_size = 334000


@ConfigRegistry.register(HarnessType.Custom, AccuracyTarget.k_99, PowerSetting.MaxQ)
class A100_SXM_80GBx4_MaxQ(A100_SXM_80GBx4):
    _system_alias = "DGX Station A100 - Red October"
    _notes = "This should not inherit from A100_SXM_80GB (DGX-A100), and cannot use start_from_device"

    numa_config = "3:0-7,32-39&2:8-15,40-47&1:16-23,48-55&0:24-31,56-63"
    power_limit = 250


@ConfigRegistry.register(HarnessType.Custom, AccuracyTarget.k_99_9, PowerSetting.MaxQ)
class A100_SXM_80GBx4_HighAccuracy_MaxQ(A100_SXM_80GBx4_MaxQ):
    pass


@ConfigRegistry.register(HarnessType.Triton, AccuracyTarget.k_99, PowerSetting.MaxQ)
class A100_SXM_80GBx4_Triton_MaxQ(A100_SXM_80GBx4_MaxQ):
    buffer_manager_thread_count = 8
    use_triton = True


@ConfigRegistry.register(HarnessType.Triton, AccuracyTarget.k_99_9, PowerSetting.MaxQ)
class A100_SXM_80GBx4_HighAccuracy_Triton_MaxQ(A100_SXM_80GBx4_Triton_MaxQ):
    pass


@ConfigRegistry.register(HarnessType.Custom, AccuracyTarget.k_99, PowerSetting.MaxP)
class A100_SXM_80GBx8(OfflineGPUBaseConfig):
    system = KnownSystem.A100_SXM_80GBx8
    complete_threads = 1
    gemm_plugin_fairshare_cache_size = 18
    gpu_batch_size = 334000
    offline_expected_qps = 2400000
    max_pairs_per_staging_thread = 262100
    start_from_device = True
    use_jemalloc = True


@ConfigRegistry.register(HarnessType.Custom, AccuracyTarget.k_99_9, PowerSetting.MaxP)
class A100_SXM_80GBx8_HighAccuracy(A100_SXM_80GBx8):
    pass


@ConfigRegistry.register(HarnessType.Triton, AccuracyTarget.k_99, PowerSetting.MaxP)
class A100_SXM_80GBx8_Triton(A100_SXM_80GBx8):
    gpu_batch_size = 262100
    offline_expected_qps = 2450000
    batch_triton_requests = True
    use_triton = True
    num_concurrent_batchers = 1


@ConfigRegistry.register(HarnessType.Triton, AccuracyTarget.k_99_9, PowerSetting.MaxP)
class A100_SXM_80GBx8_HighAccuracy_Triton(A100_SXM_80GBx8_Triton):
    gpu_batch_size = 334000
    offline_expected_qps = 2400000


@ConfigRegistry.register(HarnessType.Custom, AccuracyTarget.k_99, PowerSetting.MaxQ)
class A100_SXM_80GBx8_MaxQ(A100_SXM_80GBx8):
    power_limit = 275


@ConfigRegistry.register(HarnessType.Custom, AccuracyTarget.k_99_9, PowerSetting.MaxQ)
class A100_SXM_80GBx8_HighAccuracy_MaxQ(A100_SXM_80GBx8_MaxQ):
    pass


@ConfigRegistry.register(HarnessType.Triton, AccuracyTarget.k_99, PowerSetting.MaxQ)
class A100_SXM_80GBx8_Triton_MaxQ(A100_SXM_80GBx8_MaxQ):
    offline_expected_qps = 2000000
    batch_triton_requests = True
    use_triton = True


@ConfigRegistry.register(HarnessType.Triton, AccuracyTarget.k_99_9, PowerSetting.MaxQ)
class A100_SXM_80GBx8_HighAccuracy_Triton_MaxQ(A100_SXM_80GBx8_Triton_MaxQ):
    pass


@ConfigRegistry.register(HarnessType.Custom, AccuracyTarget.k_99, PowerSetting.MaxP)
class A100_SXM_80GB_aarch64x1(OfflineGPUBaseConfig):
    system = KnownSystem.A100_SXM_80GB_ARMx1
    complete_threads = 1
    deque_timeout_usec = 1
    gemm_plugin_fairshare_cache_size = 18
    gpu_batch_size = 315000
    offline_expected_qps = 318000
    max_pairs_per_staging_thread = 262100
    num_staging_batches = 8
    num_staging_threads = 8
    use_jemalloc = True
    use_small_tile_gemm_plugin = True


@ConfigRegistry.register(HarnessType.Custom, AccuracyTarget.k_99_9, PowerSetting.MaxP)
class A100_SXM_80GB_aarch64x1_HighAccuracy(A100_SXM_80GB_aarch64x1):
    pass


@ConfigRegistry.register(HarnessType.Triton, AccuracyTarget.k_99, PowerSetting.MaxP)
class A100_SXM_80GB_aarch64x1_Triton(A100_SXM_80GB_aarch64x1):
    batch_triton_requests = True
    buffer_manager_thread_count = 0
    gather_kernel_buffer_threshold = 2
    use_triton = True


@ConfigRegistry.register(HarnessType.Triton, AccuracyTarget.k_99_9, PowerSetting.MaxP)
class A100_SXM_80GB_aarch64x1_HighAccuracy_Triton(A100_SXM_80GB_aarch64x1_Triton):
    pass


@ConfigRegistry.register(HarnessType.Custom, AccuracyTarget.k_99, PowerSetting.MaxP)
class A100_SXM_80GB_aarch64x8(OfflineGPUBaseConfig):
    system = KnownSystem.A100_SXM_80GB_ARMx8
    complete_threads = 1
    deque_timeout_usec = 1
    gemm_plugin_fairshare_cache_size = 18
    gpu_batch_size = 315000
    offline_expected_qps = 2400000
    max_pairs_per_staging_thread = 262100
    num_staging_batches = 8
    num_staging_threads = 8
    start_from_device = True
    use_jemalloc = True
    use_small_tile_gemm_plugin = True


@ConfigRegistry.register(HarnessType.Custom, AccuracyTarget.k_99, PowerSetting.MaxQ)
class A100_SXM_80GB_aarch64x8_MaxQ(A100_SXM_80GB_aarch64x8):
    offline_expected_qps = 2000000
    power_limit = 250


@ConfigRegistry.register(HarnessType.Custom, AccuracyTarget.k_99_9, PowerSetting.MaxQ)
class A100_SXM_80GB_aarch64x8_HighAccuracy_MaxQ(A100_SXM_80GB_aarch64x8_MaxQ):
    pass


@ConfigRegistry.register(HarnessType.Custom, AccuracyTarget.k_99_9, PowerSetting.MaxP)
class A100_SXM_80GB_aarch64x8_HighAccuracy(A100_SXM_80GB_aarch64x8):
    pass


@ConfigRegistry.register(HarnessType.Triton, AccuracyTarget.k_99, PowerSetting.MaxP)
class A100_SXM_80GB_aarch64x8_Triton(A100_SXM_80GB_aarch64x8):
    gpu_batch_size = 315000
    offline_expected_qps = 2400000
    batch_triton_requests = True
    use_triton = True
    num_concurrent_batchers = 1


@ConfigRegistry.register(HarnessType.Triton, AccuracyTarget.k_99_9, PowerSetting.MaxP)
class A100_SXM_80GB_aarch64x8_HighAccuracy_Triton(A100_SXM_80GB_aarch64x8_Triton):
    pass


@ConfigRegistry.register(HarnessType.Custom, AccuracyTarget.k_99, PowerSetting.MaxP)
class A100_SXM_80GB_aarch64_MIG_1x1g10gb(OfflineGPUBaseConfig):
    system = KnownSystem.A100_SXM_80GB_ARM_MIG_1x1g_10gb
    complete_threads = 2
    deque_timeout_usec = 1
    embedding_weights_on_gpu_part = 0.3
    gemm_plugin_fairshare_cache_size = 18
    gpu_batch_size = 51200
    offline_expected_qps = 40000
    max_pairs_per_staging_thread = 51200
    num_staging_batches = 4
    num_staging_threads = 4
    use_jemalloc = True
    use_small_tile_gemm_plugin = True


@ConfigRegistry.register(HarnessType.HeteroMIG, AccuracyTarget.k_99, PowerSetting.MaxP)
class A100_SXM_80GB_aarch64_MIG_1x1g10gb_Hetero(A100_SXM_80GB_aarch64_MIG_1x1g10gb):
    pass


@ConfigRegistry.register(HarnessType.Custom, AccuracyTarget.k_99_9, PowerSetting.MaxP)
class A100_SXM_80GB_aarch64_MIG_1x1g10gb_HighAccuracy(A100_SXM_80GB_aarch64_MIG_1x1g10gb):
    pass


@ConfigRegistry.register(HarnessType.HeteroMIG, AccuracyTarget.k_99_9, PowerSetting.MaxP)
class A100_SXM_80GB_aarch64_MIG_1x1g10gb_Hetero_HighAccuracy(A100_SXM_80GB_aarch64_MIG_1x1g10gb_HighAccuracy):
    pass


@ConfigRegistry.register(HarnessType.Triton, AccuracyTarget.k_99, PowerSetting.MaxP)
class A100_SXM_80GB_aarch64_MIG_1x1g10gb_Triton(A100_SXM_80GB_aarch64_MIG_1x1g10gb):
    batch_triton_requests = True
    buffer_manager_thread_count = 8
    use_triton = True


@ConfigRegistry.register(HarnessType.Triton, AccuracyTarget.k_99_9, PowerSetting.MaxP)
class A100_SXM_80GB_MIG_aarch64_1x1g10gb_HighAccuracy_Triton(A100_SXM_80GB_aarch64_MIG_1x1g10gb_Triton):
    pass


@ConfigRegistry.register(HarnessType.Custom, AccuracyTarget.k_99, PowerSetting.MaxP)
class A100_SXM4_40GB_MIG_1x1g5gb(OfflineGPUBaseConfig):
    system = KnownSystem.A100_SXM4_40GB_MIG_1x1g_5gb
    complete_threads = 2
    deque_timeout_usec = 1
    embedding_weights_on_gpu_part = 0.3
    gemm_plugin_fairshare_cache_size = 18
    gpu_batch_size = 51200
    offline_expected_qps = 36000
    max_pairs_per_staging_thread = 51200
    num_staging_batches = 4
    num_staging_threads = 4
    use_jemalloc = True


@ConfigRegistry.register(HarnessType.Custom, AccuracyTarget.k_99_9, PowerSetting.MaxP)
class A100_SXM4_40GB_MIG_1x1g5gb_HighAccuracy(A100_SXM4_40GB_MIG_1x1g5gb):
    pass


@ConfigRegistry.register(HarnessType.Triton, AccuracyTarget.k_99, PowerSetting.MaxP)
class A100_SXM4_40GB_MIG_1x1g5gb_Triton(A100_SXM4_40GB_MIG_1x1g5gb):
    batch_triton_requests = True
    buffer_manager_thread_count = 8
    use_triton = True
    num_concurrent_batchers = 1


@ConfigRegistry.register(HarnessType.Triton, AccuracyTarget.k_99_9, PowerSetting.MaxP)
class A100_SXM4_40GB_MIG_1x1g5gb_HighAccuracy_Triton(A100_SXM4_40GB_MIG_1x1g5gb):
    buffer_manager_thread_count = 8
    use_triton = True


@ConfigRegistry.register(HarnessType.Custom, AccuracyTarget.k_99, PowerSetting.MaxP)
class A100_SXM4_40GBx1(OfflineGPUBaseConfig):
    system = KnownSystem.A100_SXM4_40GBx1
    complete_threads = 1
    deque_timeout_usec = 1
    gemm_plugin_fairshare_cache_size = 18
    gpu_batch_size = 262100
    offline_expected_qps = 310000
    max_pairs_per_staging_thread = 262100
    num_staging_batches = 8
    num_staging_threads = 8
    start_from_device = True
    use_jemalloc = True


@ConfigRegistry.register(HarnessType.Custom, AccuracyTarget.k_99_9, PowerSetting.MaxP)
class A100_SXM4_40GBx1_HighAccuracy(A100_SXM4_40GBx1):
    pass


@ConfigRegistry.register(HarnessType.Triton, AccuracyTarget.k_99, PowerSetting.MaxP)
class A100_SXM4_40GBx1_Triton(A100_SXM4_40GBx1):
    batch_triton_requests = True
    buffer_manager_thread_count = 0
    gather_kernel_buffer_threshold = 2
    use_triton = True


@ConfigRegistry.register(HarnessType.Triton, AccuracyTarget.k_99_9, PowerSetting.MaxP)
class A100_SXM4_40GBx1_HighAccuracy_Triton(A100_SXM4_40GBx1_Triton):
    pass


@ConfigRegistry.register(HarnessType.Custom, AccuracyTarget.k_99, PowerSetting.MaxP)
class A100_SXM4_40GBx8(OfflineGPUBaseConfig):
    system = KnownSystem.A100_SXM4_40GBx8
    complete_threads = 1
    gemm_plugin_fairshare_cache_size = 18
    gpu_batch_size = 262100
    offline_expected_qps = 2120000
    max_pairs_per_staging_thread = 262100
    start_from_device = True
    use_jemalloc = True


@ConfigRegistry.register(HarnessType.Custom, AccuracyTarget.k_99_9, PowerSetting.MaxP)
class A100_SXM4_40GBx8_HighAccuracy(A100_SXM4_40GBx8):
    pass


@ConfigRegistry.register(HarnessType.Triton, AccuracyTarget.k_99, PowerSetting.MaxP)
class A100_SXM4_40GBx8_Triton(A100_SXM4_40GBx8):
    offline_expected_qps = 1900000
    batch_triton_requests = True
    use_triton = True
    num_concurrent_batchers = 1


@ConfigRegistry.register(HarnessType.Triton, AccuracyTarget.k_99_9, PowerSetting.MaxP)
class A100_SXM4_40GBx8_HighAccuracy_Triton(A100_SXM4_40GBx8_Triton):
    pass


@ConfigRegistry.register(HarnessType.Custom, AccuracyTarget.k_99, PowerSetting.MaxP)
class A30_MIG_1x1g6gb(OfflineGPUBaseConfig):
    system = KnownSystem.A30_MIG_1x1g_6gb
    use_small_tile_gemm_plugin = True
    complete_threads = 1
    deque_timeout_usec = 1
    embedding_weights_on_gpu_part = 0.1
    gemm_plugin_fairshare_cache_size = 18
    gpu_batch_size = 12800
    offline_expected_qps = 35600
    max_pairs_per_staging_thread = 12800
    num_staging_batches = 2
    num_staging_threads = 2
    use_jemalloc = True
    workspace_size = 536870912


@ConfigRegistry.register(HarnessType.Custom, AccuracyTarget.k_99_9, PowerSetting.MaxP)
class A30_MIG_1x1g6gb_HighAccuracy(A30_MIG_1x1g6gb):
    pass


@ConfigRegistry.register(HarnessType.HeteroMIG, AccuracyTarget.k_99, PowerSetting.MaxP)
class A30_MIG_1x1g6gb_Hetero(A30_MIG_1x1g6gb):
    offline_expected_qps = 33000


@ConfigRegistry.register(HarnessType.HeteroMIG, AccuracyTarget.k_99_9, PowerSetting.MaxP)
class A30_MIG_1x1g6gb_Hetero_HighAccuracy(A30_MIG_1x1g6gb_Hetero):
    pass


@ConfigRegistry.register(HarnessType.Triton, AccuracyTarget.k_99, PowerSetting.MaxP)
class A30_MIG_1x1g6gb_Triton(A30_MIG_1x1g6gb):
    batch_triton_requests = True
    buffer_manager_thread_count = 8
    use_triton = True


@ConfigRegistry.register(HarnessType.Triton, AccuracyTarget.k_99, PowerSetting.MaxP)
class A30_MIG_32x1g6gb_Triton(A30_MIG_1x1g6gb):
    system = KnownSystem.A30_MIG_32x1g_6gb
    offline_expected_qps = 1088000
    batch_triton_requests = True
    buffer_manager_thread_count = 8
    use_triton = True


@ConfigRegistry.register(HarnessType.Custom, AccuracyTarget.k_99, PowerSetting.MaxP)
class A30x1(OfflineGPUBaseConfig):
    system = KnownSystem.A30x1
    complete_threads = 2
    deque_timeout_usec = 1
    embedding_weights_on_gpu_part = 0.8
    gemm_plugin_fairshare_cache_size = 18
    gpu_batch_size = 262100
    offline_expected_qps = 140000
    max_pairs_per_staging_thread = 262100
    num_staging_batches = 4
    num_staging_threads = 4
    use_jemalloc = True


@ConfigRegistry.register(HarnessType.Custom, AccuracyTarget.k_99_9, PowerSetting.MaxP)
class A30x1_HighAccuracy(A30x1):
    pass


@ConfigRegistry.register(HarnessType.Triton, AccuracyTarget.k_99, PowerSetting.MaxP)
class A30x1_Triton(A30x1):
    batch_triton_requests = True
    use_triton = True


@ConfigRegistry.register(HarnessType.Triton, AccuracyTarget.k_99_9, PowerSetting.MaxP)
class A30x1_HighAccuracy_Triton(A30x1_Triton):
    pass


@ConfigRegistry.register(HarnessType.Custom, AccuracyTarget.k_99, PowerSetting.MaxP)
class A30x8(A30x1):
    system = KnownSystem.A30x8
    offline_expected_qps = 1120000
    numa_config = "3:0-15&2:16-31&1:32-47&0:48-63&7:64-79&6:80-95&5:96-111&4:112-127"


@ConfigRegistry.register(HarnessType.Custom, AccuracyTarget.k_99_9, PowerSetting.MaxP)
class A30x8_HighAccuracy(A30x8):
    pass


@ConfigRegistry.register(HarnessType.Triton, AccuracyTarget.k_99, PowerSetting.MaxP)
class A30x8_Triton(A30x8):
    batch_triton_requests = True
    use_triton = True
    num_concurrent_batchers = 1


@ConfigRegistry.register(HarnessType.Triton, AccuracyTarget.k_99_9, PowerSetting.MaxP)
class A30x8_HighAccuracy_Triton(A30x8_Triton):
    pass


@ConfigRegistry.register(HarnessType.Custom, AccuracyTarget.k_99, PowerSetting.MaxP)
class A2x2(OfflineGPUBaseConfig):
    system = KnownSystem.A2x2
    complete_threads = 2
    deque_timeout_usec = 1
    embedding_weights_on_gpu_part = 0.5
    gemm_plugin_fairshare_cache_size = 18
    gpu_batch_size = 204000
    offline_expected_qps = 50000
    max_pairs_per_staging_thread = 262100
    num_staging_batches = 4
    num_staging_threads = 4
    use_jemalloc = True


@ConfigRegistry.register(HarnessType.Custom, AccuracyTarget.k_99_9, PowerSetting.MaxP)
class A2x2_HighAccuracy(A2x2):
    pass


@ConfigRegistry.register(HarnessType.Triton, AccuracyTarget.k_99, PowerSetting.MaxP)
class A2x2_Triton(A2x2):
    batch_triton_requests = True
    use_triton = True


@ConfigRegistry.register(HarnessType.Triton, AccuracyTarget.k_99_9, PowerSetting.MaxP)
class A2x2_HighAccuracy_Triton(A2x2_Triton):
    pass


@ConfigRegistry.register(HarnessType.Custom, AccuracyTarget.k_99, PowerSetting.MaxP)
class T4x1(OfflineGPUBaseConfig):
    system = KnownSystem.T4x1
    enable_interleaved_top_mlp = True
    output_padding_granularity = 32
    use_small_tile_gemm_plugin = False
    complete_threads = 2
    deque_timeout_usec = 1
    embedding_weights_on_gpu_part = 0.5
    gpu_batch_size = 262100
    offline_expected_qps = 34000
    max_pairs_per_staging_thread = 262100
    num_staging_batches = 4
    num_staging_threads = 4
    use_jemalloc = True


@ConfigRegistry.register(HarnessType.Custom, AccuracyTarget.k_99_9, PowerSetting.MaxP)
class T4x1_HighAccuracy(T4x1):
    pass


@ConfigRegistry.register(HarnessType.Triton, AccuracyTarget.k_99, PowerSetting.MaxP)
class T4x1_Triton(T4x1):
    batch_triton_requests = True
    buffer_manager_thread_count = 8
    use_triton = True


@ConfigRegistry.register(HarnessType.Triton, AccuracyTarget.k_99_9, PowerSetting.MaxP)
class T4x1_HighAccuracy_Triton(T4x1_Triton):
    pass


@ConfigRegistry.register(HarnessType.Custom, AccuracyTarget.k_99, PowerSetting.MaxP)
class T4x20(T4x1):
    system = KnownSystem.T4x20
    complete_threads = 8
    offline_expected_qps = 680000
    num_staging_batches = 64
    num_staging_threads = 80
    use_jemalloc = False


@ConfigRegistry.register(HarnessType.Custom, AccuracyTarget.k_99_9, PowerSetting.MaxP)
class T4x20_HighAccuracy(T4x20):
    pass


@ConfigRegistry.register(HarnessType.Triton, AccuracyTarget.k_99, PowerSetting.MaxP)
class T4x20_Triton(T4x20):
    offline_expected_qps = 360000
    batch_triton_requests = True
    use_triton = True


@ConfigRegistry.register(HarnessType.Triton, AccuracyTarget.k_99_9, PowerSetting.MaxP)
class T4x20_HighAccuracy_Triton(T4x20_Triton):
    pass


@ConfigRegistry.register(HarnessType.Custom, AccuracyTarget.k_99, PowerSetting.MaxP)
class T4x8(T4x1):
    system = KnownSystem.T4x8
    complete_threads = 8
    offline_expected_qps = 272000
    num_staging_batches = 16
    num_staging_threads = 16


@ConfigRegistry.register(HarnessType.Custom, AccuracyTarget.k_99_9, PowerSetting.MaxP)
class T4x8_HighAccuracy(T4x8):
    pass


@ConfigRegistry.register(HarnessType.Triton, AccuracyTarget.k_99, PowerSetting.MaxP)
class T4x8_Triton(T4x8):
    offline_expected_qps = 254000
    use_triton = True


@ConfigRegistry.register(HarnessType.Triton, AccuracyTarget.k_99_9, PowerSetting.MaxP)
class T4x8_HighAccuracy_Triton(T4x8_Triton):
    pass
