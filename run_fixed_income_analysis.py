"""Run the saved Fixed Income notebook offline in this Python environment."""
from datetime import datetime
from pathlib import Path
import shutil
import sys

import nbformat
from nbclient import NotebookClient
from jupyter_client import KernelManager


def main():
    root = Path(__file__).resolve().parent
    notebook_path = root / "fixed_income.ipynb"
    backup = root / "backups" / ("fixed_income_run_" + datetime.now().strftime("%Y%m%d_%H%M%S_%f"))
    backup.mkdir(parents=True)
    shutil.copy2(notebook_path, backup / notebook_path.name)
    output = root / "outputs" / "fixed_income"
    if output.exists():
        shutil.copytree(output, backup / "outputs")
    notebook = nbformat.read(notebook_path, as_version=4)
    manager = KernelManager(kernel_name="python3")
    manager.kernel_spec.argv = [sys.executable, "-m", "ipykernel_launcher", "-f", "{connection_file}"]
    client = NotebookClient(notebook, km=manager, timeout=180,
                            resources={"metadata": {"path": str(root)}})
    try:
        client.execute()
        nbformat.write(notebook, notebook_path)
    finally:
        if manager.has_kernel:
            manager.shutdown_kernel(now=True)
    print(f"Executed all cells: {notebook_path}\nPrevious version: {backup}")


if __name__ == "__main__":
    main()
