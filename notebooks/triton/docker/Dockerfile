FROM mcr.microsoft.com/azureml/aml-triton

RUN pip install azureml-core azureml-defaults azureml-contrib-services
RUN pip install numpy inference-schema[numpy-support] pillow
RUN pip install nvidia-pyindex
RUN pip install tritonclient[http]
