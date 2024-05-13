# RoamML

## RoamML WiFi Experiment setup

1. Install [mininet-wifi](https://mininet-wifi.github.io/get-started/)

2. Download the 'latest' zip file from [this link](https://drive.google.com/drive/u/0/folders/1jszVdx2FazdqE9j1G1tGNxb2yPNfpU2m) and extract the folders 'datasets', 'json_nodes' and 'models' within this directory.

3. Create a python virtual environment with pip, and install the dependencies:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

4. Run the Experiment:
    ```bash
    sudo python mininet-wifi-olsr2.py
    ```
