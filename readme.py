# imports
<<<<<<< HEAD
=======
import os
>>>>>>> 2b4678afbd065956b57d110fc17ba97e0b140624
import json
import glob
import argparse

<<<<<<< HEAD
# setup argparse
parser = argparse.ArgumentParser()
args = parser.parse_args()

# constants, variables, parameters, etc.
with open("docs/data/prefix.data", "r") as f:
    prefix = f.read()
with open("docs/data/suffix.data", "r") as f:
    suffix = f.read()

training_table = """
**Training examples**
path|compute|environment|description
-|-|-|-
"""

deployment_table = """
**Deployment examples**
path|compute|description
-|-|-
"""

concepts_table = """
**Concepts examples**
path|area|description
=======
# issue #146
if "posix" not in os.name:
    print(
        "windows is not supported, see issue #146 (https://github.com/Azure/azureml-examples/issues/146)"
    )
    exit(1)

# setup argparse
parser = argparse.ArgumentParser()
parser.add_argument("--check-readme", type=bool, default=False)
args = parser.parse_args()

# constants, variables, parameters, etc.
with open("data/markdowns/prefix.md", "r") as f:
    prefix = f.read()
with open("data/markdowns/suffix.md", "r") as f:
    suffix = f.read()

tutorial_table = """
**Tutorials**
path|status|notebooks|description
-|-|-|-
"""

notebook_table = """
**Notebooks**
path|description
-|-
"""

train_table = """
**Train**
path|compute|environment|description
-|-|-|-
"""

deploy_table = """
**Deploy**
path|compute|description
>>>>>>> 2b4678afbd065956b57d110fc17ba97e0b140624
-|-|-
"""

ws = "default"
rg = "azureml-examples"
<<<<<<< HEAD
nb = "${{matrix.notebook}}"
=======
mn = "${{matrix.notebook}}"
mw = "${{matrix.workflow}}"
>>>>>>> 2b4678afbd065956b57d110fc17ba97e0b140624
cr = "${{secrets.AZ_AE_CREDS}}"

kernelspec = {"display_name": "Python 3.8", "language": "python", "name": "python3.8"}

<<<<<<< HEAD
# get list of notebooks
nbs = [
    nb
    for nb in glob.glob("*/**/*.ipynb", recursive=True)
    if "concepts" in nb or "notebooks" in nb
]

# create workflow yaml file
workflow = f"""name: run-notebooks
on: [push]
=======
# process tutorials/*
tutorials = sorted(glob.glob("tutorials/*"))

for tutorial in tutorials:

    # get list of notebooks
    nbs = sorted(
        [nb.split("/")[-1] for nb in glob.glob(f"{tutorial}/*.ipynb")]
    )  # TODO: fix for Windows
    nbs = [f"[{nb}]({tutorial}/{nb})" for nb in nbs]  # TODO: fix for Windows
    nbs = "<br>".join(nbs)

    # get the tutorial name and initials
    name = tutorial.split("/")[-1]  # TODO: fix for Windows
    initials = "".join([word[0][0] for word in name.split("-")])

    # build entries for tutorial table
    status = f"[![{name}](https://github.com/Azure/azureml-examples/workflows/run-tutorial-{initials}/badge.svg)](https://github.com/Azure/azureml-examples/actions?query=workflow%3Arun-tutorial-{initials})"
    desc = "*no description*"
    try:
        with open(f"{tutorial}/README.md", "r") as f:
            for line in f.readlines():
                if "description: " in str(line):
                    desc = line.split(": ")[-1].strip()
                    break
    except:
        pass

    # add row to tutorial table
    tutorial_table += f"[{name}]({tutorial})|{status}|{nbs}|{desc}\n"

# process notebooks/*
notebooks = sorted(glob.glob("notebooks/**.ipynb"))

# create `run-workflows` workflow yaml file
workflow = f"""name: run-notebooks
on:
  push: 
    branches:
      - main
    paths:
      - "notebooks/**"
  pull_request:
    branches:
      - main
    paths:
      - "notebooks/**"
  schedule:
      - cron: "0 0/2 * * *"
>>>>>>> 2b4678afbd065956b57d110fc17ba97e0b140624
jobs:
  build:
    runs-on: ubuntu-latest 
    strategy:
      matrix:
<<<<<<< HEAD
        notebook: {nbs}
=======
        notebook: {notebooks}
>>>>>>> 2b4678afbd065956b57d110fc17ba97e0b140624
    steps:
    - name: check out repo
      uses: actions/checkout@v2
    - name: setup python
      uses: actions/setup-python@v2
<<<<<<< HEAD
    - name: pip install
      run: pip install -r requirements.txt
    - name: check code format
      run: black --check .
    - name: check notebook format
      run: black-nb --clear-output --check .
=======
      with: 
        python-version: "3.8"
    - name: pip install
      run: pip install -r requirements.txt
>>>>>>> 2b4678afbd065956b57d110fc17ba97e0b140624
    - name: azure login
      uses: azure/login@v1
      with:
        creds: {cr}
    - name: install azmlcli
<<<<<<< HEAD
      run: az extension add -n azure-cli-ml
    - name: attach to workspace
      run: az ml folder attach -w {ws} -g {rg}
    - name: run notebook
      run: papermill {nb} out.ipynb -k python
"""

=======
      run: az extension add -s https://azurecliext.blob.core.windows.net/release/azure_cli_ml-1.15.0-py3-none-any.whl -y
    - name: attach to workspace
      run: az ml folder attach -w {ws} -g {rg}
    - name: run notebook
      run: papermill {mn} out.ipynb -k python
"""

# write `run-notebooks` workflow yaml file
>>>>>>> 2b4678afbd065956b57d110fc17ba97e0b140624
print("writing workflow file...")
with open(f".github/workflows/run-notebooks.yml", "w") as f:
    f.write(workflow)

<<<<<<< HEAD
# create README.md file
for nb in nbs:
=======
# create notebook_table
for nb in notebooks:

    # read in notebook
    with open(nb, "r") as f:
        data = json.load(f)

    # read in the description
    try:
        if "description: " in str(data["cells"][0]["source"]):
            desc = (
                str(data["cells"][0]["source"])
                .split("description: ")[-1]
                .replace("']", "")
                .strip()
            )
    except:
        desc = "*no description*"

    # build tables
    notebook_table += f"[{nb}]({nb})|{desc}\n"

# process code/azureml/*
workflows = sorted(glob.glob("workflows/**/*.py"))

# create `run-workflows` workflow yaml file
workflow = f"""name: run-workflows
on:
  push: 
    branches:
      - main
    paths:
      - "workflows/**"
      - "code/**"
      - "environments/**"
      - "mlprojects/**"
      - "data/**"
  pull_request:
    branches:
      - main
    paths:
      - "workflows/**"
      - "code/**"
      - "environments/**"
      - "mlprojects/**"
      - "data/raw/**"
  schedule:
      - cron: "0 0/2 * * *"
jobs:
  build:
    runs-on: ubuntu-latest 
    strategy:
      matrix:
        workflow: {workflows}
    steps:
    - name: check out repo
      uses: actions/checkout@v2
    - name: setup python
      uses: actions/setup-python@v2
      with: 
        python-version: "3.8"
    - name: pip install
      run: pip install -r requirements.txt
    - name: azure login
      uses: azure/login@v1
      with:
        creds: {cr}
    - name: install azmlcli
      run: az extension add -s https://azurecliext.blob.core.windows.net/release/azure_cli_ml-1.15.0-py3-none-any.whl -y
    - name: attach to workspace
      run: az ml folder attach -w {ws} -g {rg}
    - name: run workflow 
      run: python {mw}
"""

# write `run-workflows` workflow yaml file
print("writing workflow file...")
with open(f".github/workflows/run-workflows.yml", "w") as f:
    f.write(workflow)

# create example tables
for wf in workflows:

    # read in example
    with open(wf, "r") as f:
        data = f.read()

        # read in the description
        try:
            desc = data.split("\n")[0].split(": ")[-1].strip()
        except:
            desc = "*no description*"

        # build tables
        if "train" in wf:
            # parse for compute target
            if "cpu-cluster" in data:
                compute = "AML - CPU"
            elif "gpu-cluster" in data or "gpu-K80" in data or "gpu-V100" in data:
                compute = "AML - GPU"
            else:
                compute = "unknown"
            # parse for environment type
            if "Environment.from_pip_requirements" in data:
                environment = "pip"
            elif "Environment.from_conda_specification" in data:
                environment = "conda"
            elif "env.docker.base_dockerfile" in data:
                environment = "docker"
            elif "mlproject" in wf:
                environment = "mlproject"
            else:
                environment = "unknown"
            train_table += f"[{wf}]({wf})|{compute}|{environment}|{desc}\n"
        elif "deploy" in wf:
            if "aci-cpu" in wf:
                compute = "ACI - CPU"
            elif "aks-cpu" in wf:
                compute = "AKS - CPU"
            elif "aks-gpu" in wf:
                compute = "AKS - GPU"
            elif "local" in wf:
                compute = "local"
            else:
                compute = "unknown"
            deploy_table += f"[{wf}]({wf})|{compute}|{desc}\n"

# glob all notebooks
notebooks = sorted(glob.glob("**/**/*.ipynb"))

# process all notebooks and rewrite
for nb in notebooks:
>>>>>>> 2b4678afbd065956b57d110fc17ba97e0b140624

    # read in notebook
    with open(nb, "r") as f:
        data = json.load(f)

    # update metadata
    data["metadata"]["kernelspec"] = kernelspec

    # write notebook
    with open(nb, "w") as f:
<<<<<<< HEAD
        json.dump(data, f, indent=2)

    # read in the description
    if "description: " in str(data["cells"][0]["source"]):
        desc = (
            str(data["cells"][0]["source"])
            .split("description: ")[-1]
            .replace("']", "")
            .strip()
        )
    else:
        desc = "*no description*"

    # build tables
    if "train" in nb:
        if "cpu-cluster" in str(data):
            compute = "AML - CPU"
        elif (
            "gpu-cluster" in str(data)
            or "gpu-K80" in str(data)
            or "gpu-V100" in str(data)
        ):
            compute = "AML - GPU"
        else:
            compute = "Unknown"
        if "Environment.from_pip_requirements" in str(data):
            environment = "pip"
        elif "Environment.from_conda_specification" in str(data):
            environment = "conda"
        elif "env.docker.base_dockerfile" in str(data):
            environment = "docker"
        elif "mlproject" in nb:
            environment = "mlproject"
        else:
            environment = "unknown"

        training_table += f"[{nb}]({nb})|{compute}|{environment}|{desc}\n"
    elif "deploy" in nb:
        if "aks-cpu-deploy" in str(data):
            compute = "AKS - CPU"
        elif "aks-gpu-deploy" in str(data):
            compute = "AKS - GPU"
        elif "local" in nb:
            compute = "local"
        else:
            compute = "unknown"

        deployment_table += f"[{nb}]({nb})|{compute}|{desc}\n"
    elif "concepts" in nb:
        area = nb.split("/")[-2]
        concepts_table += f"[{nb}]({nb})|{area}|{desc}\n"

print("writing README.md...")
with open("README.md", "w") as f:
    f.write(prefix + training_table + deployment_table + concepts_table + suffix)
=======
        json.dump(data, f, indent=1)

# run code formatter on .py files
os.system("black .")

# run code formatter on .ipynb files
os.system("black-nb --clear-output .")

# read in README.md for comparison
with open("README.md", "r") as f:
    before = f.read()

# write README.md file
print("writing README.md...")
with open("README.md", "w") as f:
    f.write(
        prefix + tutorial_table + notebook_table + train_table + deploy_table + suffix
    )

# read in README.md for comparison
with open("README.md", "r") as f:
    after = f.read()

# check if README.md file matches before and after
if args.check_readme and before != after:
    print("README.md file did not match...")
    exit(2)
>>>>>>> 2b4678afbd065956b57d110fc17ba97e0b140624
