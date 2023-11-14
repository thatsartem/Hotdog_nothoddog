import torch
from torchvision.models import resnet50
from PIL import Image
import io

from transform import test_transform, topil

classes = ["hotdog", "nothotdog"]
model = resnet50(pretrained=True)
model.fc = torch.nn.Sequential(
    torch.nn.Linear(in_features=2048, out_features=10),
    torch.nn.ReLU(),
    torch.nn.Linear(in_features=10, out_features=2),
    torch.nn.Softmax(1),
)

config = torch.load("hotdog_0.8894230769230769.pth", map_location=torch.device("cpu"))
model.load_state_dict(config["model_state_dict"])

model.eval()


def predict(raw_img):
    with Image.open(raw_img) as img:
        img.save("test.jpg")
        tensor = test_transform(img)
        topil(tensor).save("test1.jpg")
        with torch.no_grad():
            out = model(tensor.unsqueeze(0))
            print(out)
            result = classes[torch.argmax(out)]
        return result
