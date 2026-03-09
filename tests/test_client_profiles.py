import json
import sys
from pathlib import Path
import importlib.util
from unittest.mock import MagicMock

# Mock streamlit before importing the module
mock_st = MagicMock()
sys.modules["streamlit"] = mock_st

def import_client_profiles():
    # Path to the module with emoji
    module_path = Path("pages/2_🎨_Client_Profiles.py")
    spec = importlib.util.spec_from_file_location("client_profiles", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

client_profiles = import_client_profiles()

def test_load_clients_creates_dir(tmp_path, monkeypatch):
    # Setup: Use tmp_path as the working directory
    monkeypatch.chdir(tmp_path)

    # Ensure "clients" directory doesn't exist
    clients_dir = tmp_path / "clients"
    assert not clients_dir.exists()

    # Run
    clients = client_profiles.load_clients()

    # Assert
    assert clients_dir.exists()
    assert clients_dir.is_dir()
    assert clients == {}

def test_load_clients_loads_files(tmp_path, monkeypatch):
    # Setup: Use tmp_path as the working directory
    monkeypatch.chdir(tmp_path)
    clients_dir = tmp_path / "clients"
    clients_dir.mkdir()

    # Create some dummy client files
    client1_data = {"name": "Client One", "theme": {"primary": "#111"}}
    client2_data = {"name": "Client Two", "theme": {"primary": "#222"}}

    (clients_dir / "client1.json").write_text(json.dumps(client1_data))
    (clients_dir / "client2.json").write_text(json.dumps(client2_data))

    # Run
    clients = client_profiles.load_clients()

    # Assert
    assert len(clients) == 2
    assert "client1" in clients
    assert "client2" in clients

    assert clients["client1"]["name"] == "Client One"
    assert Path(clients["client1"]["_filepath"]).resolve() == (clients_dir / "client1.json").resolve()

    assert clients["client2"]["name"] == "Client Two"
    assert Path(clients["client2"]["_filepath"]).resolve() == (clients_dir / "client2.json").resolve()

def test_load_clients_empty_dir(tmp_path, monkeypatch):
    # Setup
    monkeypatch.chdir(tmp_path)
    clients_dir = tmp_path / "clients"
    clients_dir.mkdir()

    # Run
    clients = client_profiles.load_clients()

    # Assert
    assert clients == {}
