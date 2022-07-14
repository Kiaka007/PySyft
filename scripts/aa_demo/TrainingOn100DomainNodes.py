#!/usr/bin/env python
# coding: utf-8


# stdlib
import time

# third party
import pandas as pd

# syft absolute
import syft as sy
from syft import nn

DOMAIN_INFO_FILE = "test.csv"
USER_EMAIL = "sam@stargate.net"
USER_PASSWORD = "changethis"


def get_domain_addresses():
    domain_info = pd.read_csv(DOMAIN_INFO_FILE, header=None)
    ip_addresses = domain_info[0].values.tolist()
    return ip_addresses


def initialize_model(input_shape) -> nn.Model:

    # create an empty model
    model = nn.Model()

    # Add layers to the model

    # Layer 1
    model.add(nn.Convolution(nb_filter=32, filter_size=3, padding=2, input_shape=input_shape))
    model.add(nn.BatchNorm(activation=nn.leaky_ReLU()))
    model.add(nn.MaxPool(pool_size=2, stride=2))

    # Layer 2
    model.add(nn.Convolution(nb_filter=64, filter_size=3, padding=2))
    model.add(nn.BatchNorm(activation=nn.leaky_ReLU()))
    model.add(nn.MaxPool(pool_size=2, stride=2))

    # Layer 3
    model.add(nn.AvgPool(3))

    # Layer 4
    model.add(nn.Flatten())

    # Layer 5
    model.add(nn.Linear(2, 512))

    model.initialize_weights()

    return model


def get_input_shape(domain_address):
    domain = sy.login(url=domain_address, email=USER_EMAIL, password=USER_PASSWORD)
    X_train = domain.datasets[-1]["train_images"][:2]  # just taking first two images.
    return X_train.public_shape



def train_on_domains(domain_addresses):
    """Remotely train on the list of domains."""

    # TRAINING PARAMS
    n_epochs = 1
    batch_size = 2

    # Get input shape of the images
    # We assume images on all domains have the same shape.
    input_shape = get_input_shape(domain_addresses[0])  # Shape Format -> (N, C, H, W)

    print("Input Shape: ", input_shape)

    # initialize the model
    model = initialize_model(input_shape=input_shape)

    for i, address in enumerate(domain_addresses):

        # Log into the domain
        domain = sy.login(url=address, email=USER_EMAIL, password=USER_PASSWORD)

        print(f"Domain: {i+1} - {domain.name}")

        # Check if dataset is present on the domain
        if len(domain.datasets) == 0:
            print(f"Error on domain = {domain.name} with address = {address}")
            continue

        # Get pointers to images and labels
        X_train = domain.datasets[-1]["train_images"][:2]
        y_train = domain.datasets[-1]["train_labels"][:2]

        print(f"Image Shape: {X_train.public_shape}, Label Shape: {y_train.public_shape}")

        # Perform a single epoch
        model_ptr = model.send(domain,send_to_blob_storage=False)

        # Perform a single step
        # A single step performs the following operation on the batch of images:
        # - forward pass
        # - calculates loss
        # - backward pass
        # - optimizer weight updates
        print(f"Training started on Domain: {i+1} - {domain.name}")
        run_status = model_ptr.step(X_train, y_train)

        # Wait for step operation to be completed on the remote domain.
        while(not run_status.exists):
            time.sleep(10)

        # Publish Model Weights
        print(f"Publishing model weights on Domain: {i+1} - {domain.name}")
        published_obj = model_ptr.publish(sigma=1e4)  # PB spent with 1e3 = 690k, thus 1e4 sigma -> 6.9k which is within PB limit of 9999
        while(not published_obj.exists):
            time.sleep(2)
        new_weights = published_obj.get_copy()

        # Update weights and move onto next domain node
        model = initialize_model(input_shape)
        model.replace_weights(new_weights)
        print(f"Model training finished on Domain: {i+1} - {domain.name}")

        print()

    return model


if __name__ == "__main__":
    domain_host_ips = get_domain_addresses()
    final_model = train_on_domains(domain_host_ips)

