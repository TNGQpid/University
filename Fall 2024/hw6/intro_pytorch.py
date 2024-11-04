import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms



def get_data_loader(training = True):
    """
    TODO: implement this function.

    INPUT: 
        An optional boolean argument (default value is True for training dataset)

    RETURNS:
        Dataloader for the training set (if training = True) or the test set (if training = False)
    """
    transform=transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
        ])

    training_data = datasets.FashionMNIST(
    root="data",
    train=True,
    download=True,
    transform=transform
    )

    test_data = datasets.FashionMNIST(
    root="data",
    train=False,
    download=True,
    transform=transform
    )

    DataLoader = torch.utils.data.DataLoader
    train_dataloader = DataLoader(training_data, batch_size=64)
    test_dataloader = DataLoader(test_data, batch_size=64)
    
    if training:
        return train_dataloader
    else:
        return test_dataloader


def build_model():
    """
    TODO: implement this function.

    INPUT: 
        None

    RETURNS:
        An untrained neural network model
    """
    model = nn.Sequential(
        nn.Flatten(),
        nn.Linear(28*28, 128),
        nn.ReLU(),
        nn.Linear(128, 64),
        nn.ReLU(),
        nn.Linear(64, 10),
        )
    return model



def train_model(model, train_loader, criterion, T):
    """
    TODO: implement this function.

    INPUT: 
        model - the model produced by the previous function
        train_loader  - the train DataLoader produced by the first function
        criterion   - cross-entropy 
        T - number of epochs for training

    RETURNS:
        None
    """
    def train_step(model, train_loader, criterion):
            # Set the model to training mode - important for batch normalization and dropout layers
            # Unnecessary in this situation but added for best practices
            model.train()
    
            correct = 0  # To keep track of correct predictions
            total = 0    # Total number of samples
            total_loss = 0
    
            otim = torch.optim.SGD(model.parameters(), lr=0.001, momentum=0.9)
            for batch, (X, y) in enumerate(train_loader):
                batch_size = X.size(0)
                # Compute prediction and loss
                pred = model(X)
    
                otim.zero_grad()
                
                loss = criterion(pred, y)
                total_loss += loss.item()
                # include an optimizer
                
                # Backpropagation
                loss.backward()
                otim.step()
                
                # find the predicted class of each item in the batch:
                predicted = pred.argmax(1)
                # if it's the correct class, make it a 1. Then find the sum to see how many we got correct
                to_add = (predicted == y).sum()
                # update current to include the newly classified batch
                correct += to_add
                total += batch_size

            los = total_loss / len(train_loader)
            
            return los, correct, total

    size = len(train_loader.dataset)
    for epoch in range(T):
        loss, correct, total = train_step(model, train_loader, criterion)
        print(f"Train Epoch: {epoch}      Accuracy: {correct}/{total} ({correct/total*100:.2f}%)     Loss: {loss:.3f}")
        

def evaluate_model(model, test_loader, criterion, show_loss = True):
    """
    TODO: implement this function.

    INPUT: 
        model - the the trained model produced by the previous function
        test_loader    - the test DataLoader
        criterion   - cropy-entropy 

    RETURNS:
        None
    """
    model.eval()
    size = len(test_loader.dataset)
    num_batches = len(test_loader)
    loss, correct = 0, 0

    # Evaluating the model with torch.no_grad() ensures that no gradients are computed during test mode
    # also serves to reduce unnecessary gradient computations and memory usage for tensors with requires_grad=True
    with torch.no_grad():
        for X, y in test_loader:
            pred = model(X)
            loss += criterion(pred, y).item()
            correct += (pred.argmax(1) == y).type(torch.float).sum().item() # the same thing as before just more compact

    loss /= num_batches
    correct /= size
    if show_loss:
        print(f"Average loss: {loss:.4f}\nAccuracy: {(100*correct):.2f}%")
    else:
        print(f"Accuracy: {(100*correct):.2f}%")


def predict_label(model, test_images, index):
    """
    TODO: implement this function.

    INPUT: 
        model - the trained model
        test_images   -  a tensor. test image set of shape Nx1x28x28
        index   -  specific index  i of the image to be tested: 0 <= i <= N - 1


    RETURNS:
        None
    """
    logits = model(test_images[index])
    prob = F.softmax(logits, dim = 1)

    class_names = ['T-shirt/top','Trouser','Pullover','Dress','Coat','Sandal','Shirt','Sneaker','Bag','Ankle Boot']
    
    # find the top 3 values and match them to the classes
    listy = [p.item() for p in prob[0]]
    top_3 = sorted(listy)[-3:]
    both = [(value, class_names[listy.index(value)]) for value in top_3]
    print(f"{both[2][1]}: {both[2][0] * 100:.2f}%\n{both[1][1]}: {both[1][0] * 100:.2f}%\n{both[0][1]}: {both[0][0] * 100:.2f}%")

if __name__ == '__main__':
    '''
    Feel free to write your own test code here to exaime the correctness of your functions. 
    Note that this part will not be graded.
    '''
    criterion = nn.CrossEntropyLoss()
