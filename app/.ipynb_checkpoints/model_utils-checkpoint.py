import torch
from torchvision import transforms
from torchvision.models import resnet18, ResNet18_Weights

class_names = ['No tumor', 'Glioma', 'Meningioma', 'Pituitary']

def load_model():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = resnet18(weights=ResNet18_Weights.DEFAULT)
    model.fc = torch.nn.Linear(model.fc.in_features, len(class_names))
    model.load_state_dict(torch.load("models/resnet_best.pth", map_location=device))
    model.to(device)
    model.eval()
    return model, device

def transform_image(image):
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.5]*3, [0.5]*3)
    ])
    return transform(image)