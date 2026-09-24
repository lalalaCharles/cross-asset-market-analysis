"""Execute every notebook cell with this Python environment, from project root."""
from datetime import datetime
from pathlib import Path
import shutil
import sys

import nbformat
from nbclient import NotebookClient
from jupyter_client import KernelManager


def main():
    root = Path(__file__).resolve().parent
    notebook_path = root / "analysis.ipynb"
    backup = root / "backups" / ("analysis_run_" + datetime.now().strftime("%Y%m%d_%H%M%S_%f"))
    backup.mkdir(parents=True)
    shutil.copy2(notebook_path, backup / notebook_path.name)
    if (root / "outputs").exists():
        shutil.copytree(root / "outputs", backup / "outputs", ignore=shutil.ignore_patterns("fixed_income"))
    notebook = nbformat.read(notebook_path, as_version=4)
    manager = KernelManager(kernel_name="python3")
    # Avoid accidentally selecting a kernel belonging to another virtualenv.
    manager.kernel_spec.argv = [sys.executable, "-m", "ipykernel_launcher", "-f", "{connection_file}"]
    client = NotebookClient(notebook, km=manager, timeout=180, resources={"metadata": {"path": str(root)}})
    try:
        client.execute()
        nbformat.write(notebook, notebook_path)
    finally:
        if manager.has_kernel:
            manager.shutdown_kernel(now=True)
    print(f"Executed all cells successfully: {notebook_path}")


if __name__ == "__main__":
    main()
