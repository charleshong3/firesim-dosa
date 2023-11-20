import subprocess
import yaml
import pathlib
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--pe_dim", type=int, default=16)
args = parser.parse_args()
pe_dim = args.pe_dim

subprocess.run(["firesim", "launchrunfarm"])
workloads = []
target_configs = []
# for i in range(773):
#     workloads.append(f"gemmini_{i}.json")
# for i in [4, 8, 16, 32, 64, 128]:
#     for t in ["matmul", "conv"]:
#         workloads.append(f"gemmini_{i}pe_{t}.json")
#         target_configs.append(f"firesim_rocket_singlecore_{i}pe4kdummygemmini_nofirstlayer_no_nic_l2_llc4mb_ddr3")
# for i in [2]:
#     for t in ["conv"]:
#         workloads.append(f"gemmini_{i}pe_{t}.json")
#         target_configs.append(f"firesim_rocket_singlecore_{i}pe4kdummygemmini_nofirstlayer_no_nic_l2_llc4mb_ddr3")
# workloads = ["gemmini_matmul.json", "gemmini_conv.json"]
if pathlib.Path("workloads/gemmini/conv_tilings-baremetal").is_file():
    workloads.append("gemmini_conv.json")
    target_configs.append(f"firesim_rocket_singlecore_{pe_dim}pe4kdummygemmini_nofirstlayer_no_nic_l2_llc4mb_ddr3")
if pathlib.Path("workloads/gemmini/matmul_tilings-baremetal").is_file():
    workloads.append("gemmini_matmul.json")
    target_configs.append(f"firesim_rocket_singlecore_{pe_dim}pe4kdummygemmini_nofirstlayer_no_nic_l2_llc4mb_ddr3")

for i in range(len(workloads)):
    config_runtime_path = "config_runtime.yaml"
    with open(config_runtime_path, "r") as f:
        config = yaml.safe_load(f)
    config["workload"]["workload_name"] = workloads[i]
    config["target_config"]["default_hw_config"] = target_configs[i]
    with open(config_runtime_path, "w") as f:
        yaml.dump(config, f)
    subprocess.run(["firesim", "infrasetup"])
    subprocess.run(["firesim", "runworkload"])

p = subprocess.Popen(["firesim", "terminaterunfarm"], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT)
p.communicate("yes\n".encode())

