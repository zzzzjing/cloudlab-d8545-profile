# -*- coding: utf-8 -*-
#!/usr/bin/env python
# CloudLab profile: single d8545 node, Ubuntu 22.04, minimal example.

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

# A tiny inline command so we can verify boot success.
node.addService(pg.Execute(shell="/bin/bash",
    command="sudo bash -lc 'echo ready > /local/READY'"))

pc.printRequestRSpec(request)
