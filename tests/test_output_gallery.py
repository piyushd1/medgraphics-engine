import os
import sys
import importlib.util
from unittest.mock import MagicMock
from pathlib import Path
from datetime import datetime
import pytest

# Mock streamlit before importing the module
sys.modules['streamlit'] = MagicMock()

# Import the module with emojis in the filename dynamically
module_name = "Output_Gallery"
module_path = os.path.join("pages", "3_🖼️_Output_Gallery.py")

spec = importlib.util.spec_from_file_location(module_name, module_path)
gallery_module = importlib.util.module_from_spec(spec)
sys.modules[module_name] = gallery_module
spec.loader.exec_module(gallery_module)

get_generated_images = gallery_module.get_generated_images

class TestGetGeneratedImages:
    """
    Tests for the get_generated_images function in the Output Gallery page.
    This suite addresses the testing gap for file system operations related to
    fetching generated PNG images.

    Coverage includes:
    - Missing directories
    - Empty directories
    - Directories with only non-PNG files
    - Directories with PNG files (verifying metadata extraction)
    - Correct sorting by modification time (newest first)
    """

    def test_missing_directory(self, tmp_path):
        """Test behavior when the output directory does not exist."""
        missing_dir = tmp_path / "non_existent_output"
        images = get_generated_images(str(missing_dir))
        assert images == []

    def test_empty_directory(self, tmp_path):
        """Test behavior when the directory exists but is empty."""
        empty_dir = tmp_path / "empty_output"
        empty_dir.mkdir()
        images = get_generated_images(str(empty_dir))
        assert images == []

    def test_no_png_files(self, tmp_path):
        """Test behavior when the directory contains files, but no PNGs."""
        no_png_dir = tmp_path / "no_png_output"
        no_png_dir.mkdir()

        # Create non-PNG files
        (no_png_dir / "test1.txt").touch()
        (no_png_dir / "test2.jpg").touch()

        images = get_generated_images(str(no_png_dir))
        assert images == []

    def test_with_png_files(self, tmp_path):
        """Test correct extraction of PNG metadata."""
        png_dir = tmp_path / "png_output"
        png_dir.mkdir()

        # Create a test PNG file
        test_file = png_dir / "test_image.png"
        test_file.touch()

        images = get_generated_images(str(png_dir))

        assert len(images) == 1
        img_data = images[0]

        assert img_data["path"] == str(test_file)
        assert img_data["filename"] == "test_image.png"
        assert "date" in img_data
        assert "timestamp" in img_data

        # Verify timestamp matches the file's actual modification time
        actual_mtime = os.path.getmtime(str(test_file))
        assert img_data["timestamp"] == actual_mtime

        # Verify date string formatting
        expected_date_str = datetime.fromtimestamp(actual_mtime).strftime("%Y-%m-%d %H:%M")
        assert img_data["date"] == expected_date_str

    def test_sorting_by_mtime(self, tmp_path, monkeypatch):
        """Test that images are returned sorted by modification time (newest first)."""
        sort_dir = tmp_path / "sort_output"
        sort_dir.mkdir()

        file1 = sort_dir / "old.png"
        file2 = sort_dir / "new.png"
        file3 = sort_dir / "oldest.png"

        file1.touch()
        file2.touch()
        file3.touch()

        # Mock os.path.getmtime to return deterministic timestamps
        def mock_getmtime(path):
            if path.endswith("old.png"):
                return 200.0
            elif path.endswith("new.png"):
                return 300.0
            elif path.endswith("oldest.png"):
                return 100.0
            return 0.0

        monkeypatch.setattr(os.path, "getmtime", mock_getmtime)

        images = get_generated_images(str(sort_dir))

        assert len(images) == 3
        # Should be newest (300) -> old (200) -> oldest (100)
        assert images[0]["filename"] == "new.png"
        assert images[1]["filename"] == "old.png"
        assert images[2]["filename"] == "oldest.png"
