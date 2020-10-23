from monitoring import ModelDataCollector
import json
import threading

def init():
    global inputs_dc, prediction_dc
    inputs_dc = ModelDataCollector(features=["timestamp", "feat1"], model_name="best_model1")
    #inputs_dc = ModelDataCollector("best_model1", designation="inputs", feature_names=["timestamp", "feat1"], collection_name='test')
    #prediction_dc = ModelDataCollector("best_model", designation="predictions", feature_names=["prediction1", "prediction2"])

def run(data):
    print(f"DEBUG: thread active count is {threading.active_count()}")
    data = json.loads(data)
    print(f"Received {data}. Should show up in App Insights logs")
    inputs_dc.collect(data)
