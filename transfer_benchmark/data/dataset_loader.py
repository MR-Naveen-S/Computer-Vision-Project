import os
import torch
import numpy as np
from torchvision import datasets, transforms
from torch.utils.data import DataLoader, Subset
import medmnist
from medmnist import INFO


def get_dataloaders(
    dataset_name="cifar10",
    batch_size=64,
    num_workers=0,
    data_cache="./data_cache",
    max_train_samples=None,
    max_test_samples=None,
    img_size=224,
    seed=42,
):
    """
    Constructs train and test DataLoaders for near-domain (CIFAR-10) and far-domain (PathMNIST)
    benchmarking datasets, standardized to (3, img_size, img_size) with ImageNet normalization.

    Args:
        dataset_name (str): 'cifar10' or 'pathmnist' (also supports 'dermamnist')
        batch_size (int): Batch size for DataLoader
        num_workers (int): Number of subprocesses for data loading (0 recommended on Windows)
        data_cache (str): Root cache directory for storing downloaded datasets
        max_train_samples (int, optional): Subsample training set for faster experimentation
        max_test_samples (int, optional): Subsample test set for faster evaluation
        img_size (int): Target spatial resolution (default: 224)
        seed (int): Random seed for reproducible subsampling

    Returns:
        tuple: (train_loader, test_loader, num_classes)
    """
    os.makedirs(data_cache, exist_ok=True)

    # Standard ImageNet normalization parameters
    mean = [0.485, 0.456, 0.406]
    std = [0.229, 0.224, 0.225]

    transform_train = transforms.Compose([
        transforms.Resize((img_size, img_size)),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize(mean=mean, std=std)
    ])

    transform_test = transforms.Compose([
        transforms.Resize((img_size, img_size)),
        transforms.ToTensor(),
        transforms.Normalize(mean=mean, std=std)
    ])

    dataset_key = dataset_name.lower().strip()

    if dataset_key == "cifar10":
        train_set = datasets.CIFAR10(
            root=data_cache, train=True, download=True, transform=transform_train
        )
        test_set = datasets.CIFAR10(
            root=data_cache, train=False, download=True, transform=transform_test
        )
        num_classes = 10

    elif dataset_key in ["pathmnist", "dermamnist", "bloodmnist"]:
        info = INFO[dataset_key]
        DataClass = getattr(medmnist, info["python_class"])
        # PathMNIST / MedMNIST RGB dataset
        train_set = DataClass(
            split="train",
            transform=transform_train,
            download=True,
            root=data_cache,
            as_rgb=True,
        )
        test_set = DataClass(
            split="test",
            transform=transform_test,
            download=True,
            root=data_cache,
            as_rgb=True,
        )
        num_classes = len(info["label"])

    else:
        raise ValueError(f"Unknown dataset: {dataset_name}. Supported: 'cifar10', 'pathmnist', 'dermamnist'")

    # Optional subsampling for rapid prototyping
    rng = np.random.RandomState(seed)

    if max_train_samples is not None and max_train_samples < len(train_set):
        train_indices = rng.choice(len(train_set), size=max_train_samples, replace=False)
        train_set = Subset(train_set, train_indices)

    if max_test_samples is not None and max_test_samples < len(test_set):
        test_indices = rng.choice(len(test_set), size=max_test_samples, replace=False)
        test_set = Subset(test_set, test_indices)

    pin_memory = torch.cuda.is_available()

    train_loader = DataLoader(
        train_set,
        batch_size=batch_size,
        shuffle=True,
        num_workers=num_workers,
        pin_memory=pin_memory,
    )
    test_loader = DataLoader(
        test_set,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=pin_memory,
    )

    return train_loader, test_loader, num_classes


if __name__ == "__main__":
    print("[*] Testing dataset_loader.py...")
    train_ld, test_ld, n_cls = get_dataloaders("cifar10", batch_size=32, max_train_samples=100, max_test_samples=50)
    img_b, lbl_b = next(iter(train_ld))
    print(f"CIFAR-10: Batch shape = {img_b.shape}, Labels shape = {lbl_b.shape}, Num classes = {n_cls}")
