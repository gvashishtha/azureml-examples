<<<<<<< HEAD
import argparse
from azureml.core import Workspace

=======
# imports
import argparse
from azureml.core import Workspace

# setup argparse
>>>>>>> 2b4678afbd065956b57d110fc17ba97e0b140624
parser = argparse.ArgumentParser()
parser.add_argument("--config", type=str, default="")
args = parser.parse_args()

<<<<<<< HEAD
ws = Workspace.from_config(args.config)

for webservice in ws.webservices:
    ws.webservices[webservice].delete()

for compute_target in ws.compute_targets:
    if "concept" in compute_target:
        ws.compute_targets[compute_target].delete()

workspaces = Workspace.list(ws.subscription_id, resource_group=ws.resource_group)
for workspace in workspaces:
    if "concept" in workspace:
        workspaces[workspace][0].delete(delete_dependent_resources=True, no_wait=True)
=======
# get workspace
ws = Workspace.from_config(args.config)

# delete all webservices
for webservice in ws.webservices:
    ws.webservices[webservice].delete()

# delete some compute targets
for compute_target in ws.compute_targets:
    if ws.compute_targets[compute_target].get_status() in ["Failed", "Canceled", None]:
        try:
            ws.compute_targets[compute_target].delete()
        except:
            pass
    elif (
        "dask-ct" in compute_target
        and ws.compute_targets[compute_target]
        .get_status()
        .serialize()["provisioningState"]
        in ["Succeeded"]
        and len(ws.compute_targets[compute_target].list_nodes()) == 0
    ):
        ws.compute_targets[compute_target].delete()
>>>>>>> 2b4678afbd065956b57d110fc17ba97e0b140624
