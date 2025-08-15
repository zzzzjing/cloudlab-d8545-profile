
# CloudLab profile for a single d8545 GPU node (Ubuntu 22.04),
# with optional: mount NVMe -> /data, run /local/repository/setup.sh on boot.
#
import geni.portal as portal
import geni.rspec.pg as pg

pc = portal.Context()

pc.defineParameter("hostname", "Node name",
                   portal.ParameterType.STRING, "gpu0")

pc.defineParameter("os_image", "Disk image URN",
                   portal.ParameterType.STRING,
                   # 常用 Ubuntu 22.04 标准镜像
                   "urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU22-64-STD")

pc.defineParameter("mount_nvme", "Format & mount local NVMe to /data",
                   portal.ParameterType.BOOLEAN, True)

pc.defineParameter("run_setup", "Run /local/repository/setup.sh at boot",
                   portal.ParameterType.BOOLEAN, True)

params = pc.bindParameters()
request = pc.makeRequestRSpec()

# ---- 单节点 d8545 ----
node = request.RawPC(params.hostname)
node.hardware_type = "d8545"
node.disk_image = params.os_image

# 开机执行 firstboot.sh（随 Profile 一起上传）
cmd_flags = []
if params.mount_nvme:
    cmd_flags.append("MOUNT_NVME=1")
if params.run_setup:
    cmd_flags.append("RUN_SETUP=1")

if cmd_flags:
    node.addService(pg.Execute(
        shell="/bin/bash",
        command="sudo /bin/bash /local/repository/firstboot.sh " + " ".join(cmd_flags)
    ))

pc.printRequestRSpec(request)

