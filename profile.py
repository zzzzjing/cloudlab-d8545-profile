
import geni.portal as portal
import geni.rspec.pg as pg

pc = portal.Context()
pc.defineParameter("hostname", "Node name",
                   portal.ParameterType.STRING, "gpu0")
pc.defineParameter("os_image", "Disk image URN",
                   portal.ParameterType.STRING,
                   "urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU22-64-STD")
params = pc.bindParameters()
request = pc.makeRequestRSpec()

node = request.RawPC(params.hostname)
node.hardware_type = "d8545"
node.disk_image = params.os_image

# 示例：一个很短的内联命令（不依赖外部脚本）
node.addService(pg.Execute(shell="/bin/bash",
    command="sudo bash -lc 'echo ready > /local/READY'"))

pc.printRequestRSpec(request)
