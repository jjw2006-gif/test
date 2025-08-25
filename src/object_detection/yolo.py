"""Simplified YOLOv1 model using PyTorch.

This module contains a light-weight implementation of the
``You Only Look Once`` (YOLO) architecture for educational
purposes.  It defines the network layers and a small training
utility that can be used with a custom dataset.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import torch
from torch import nn


class CNNBlock(nn.Module):
    """Basic convolutional block used by YOLO.

    Each block performs a convolution followed by batch
    normalisation and a LeakyReLU activation.  The original
    YOLOv1 network relies heavily on these components.
    """

    def __init__(self, in_channels: int, out_channels: int, **kwargs) -> None:
        super().__init__()
        self.conv = nn.Conv2d(in_channels, out_channels, bias=False, **kwargs)
        self.bn = nn.BatchNorm2d(out_channels)
        self.act = nn.LeakyReLU(0.1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:  # pragma: no cover - tiny utility
        return self.act(self.bn(self.conv(x)))


@dataclass
class YOLOConfig:
    """Configuration for the YOLO model."""

    split_size: int = 7
    num_boxes: int = 2
    num_classes: int = 20


class YOLOv1(nn.Module):
    """Minimal implementation of the YOLOv1 architecture."""

    def __init__(self, config: YOLOConfig | None = None) -> None:
        super().__init__()
        self.config = config or YOLOConfig()
        self.architecture = self._create_architecture()
        self.darknet = self._create_conv_layers(self.architecture)
        # output dimension is S * S * (B * 5 + C)
        S, B, C = self.config.split_size, self.config.num_boxes, self.config.num_classes
        self.fc = nn.Sequential(
            nn.Flatten(),
            nn.Linear(1024 * S * S, 4096),
            nn.Dropout(0.5),
            nn.LeakyReLU(0.1),
            nn.Linear(4096, S * S * (B * 5 + C)),
        )

    def _create_architecture(self) -> Iterable:
        return [
            (7, 64, 2, 3),
            "M",
            (3, 192, 1, 1),
            "M",
            (1, 128, 1, 0),
            (3, 256, 1, 1),
            (1, 256, 1, 0),
            (3, 512, 1, 1),
            "M",
            [(1, 256, 1, 0), (3, 512, 1, 1), 4],
            (1, 512, 1, 0),
            (3, 1024, 1, 1),
            "M",
            [(1, 512, 1, 0), (3, 1024, 1, 1), 2],
            (3, 1024, 1, 1),
            (3, 1024, 2, 1),
            (3, 1024, 1, 1),
            (3, 1024, 1, 1),
        ]

    def _create_conv_layers(self, architecture: Iterable) -> nn.Sequential:
        layers: list[nn.Module] = []
        in_channels = 3
        for x in architecture:
            if isinstance(x, tuple):
                kernel_size, filters, stride, pad = x
                layers.append(CNNBlock(in_channels, filters, kernel_size=kernel_size, stride=stride, padding=pad))
                in_channels = filters
            elif isinstance(x, str):
                layers.append(nn.MaxPool2d(kernel_size=2, stride=2))
            else:  # list
                conv1, conv2, repeat = x
                for _ in range(repeat):
                    layers.append(CNNBlock(in_channels, conv1[1], kernel_size=conv1[0], stride=conv1[2], padding=conv1[3]))
                    layers.append(CNNBlock(conv1[1], conv2[1], kernel_size=conv2[0], stride=conv2[2], padding=conv2[3]))
                    in_channels = conv2[1]
        return nn.Sequential(*layers)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.darknet(x)
        x = self.fc(x)
        S, B, C = self.config.split_size, self.config.num_boxes, self.config.num_classes
        return x.reshape(-1, S, S, B * 5 + C)


def train(model: YOLOv1, loader, optimizer, criterion, device: str = "cpu", epochs: int = 10) -> None:
    """Train the YOLO model.

    Parameters
    ----------
    model:
        The YOLO network to train.
    loader:
        Iterable returning ``(images, targets)`` pairs.
    optimizer:
        Optimiser to update the model.
    criterion:
        Loss function.
    device:
        Device on which to run the training loop.
    epochs:
        Number of passes through ``loader``.
    """

    model.to(device)
    model.train()
    for _ in range(epochs):
        for images, targets in loader:
            images = images.to(device)
            targets = targets.to(device)
            predictions = model(images)
            loss = criterion(predictions, targets)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

