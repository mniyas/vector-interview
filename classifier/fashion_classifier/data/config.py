from pathlib import Path

DATA_DIRNAME = Path(__file__).resolve().parents[3] / "input_data"
DOWNLOADED_DATA_DIRNAME = DATA_DIRNAME / "downloaded"

DIMS = (1, 28, 28)
OUTPUT_DIMS = (1,)
MAPPING = {
                 0: "T-shirt/Top",
                 1: "Trouser",
                 2: "Pullover",
                 3: "Dress",
                 4: "Coat", 
                 5: "Sandal", 
                 6: "Shirt",
                 7: "Sneaker",
                 8: "Bag",
                 9: "Ankle Boot"
                 }
TRAIN_SIZE = 55000
VAL_SIZE = 5000
