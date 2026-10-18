"""Runs the full pipeline: clean -> analyse -> build dashboard."""
import subprocess, sys
from pathlib import Path
S = Path(__file__).parent / "scripts"
for s in ["01_clean_data.py", "02_analysis_and_charts.py", "03_build_dashboard.py"]:
    print(f"\n=== Running {s} ===")
    subprocess.run([sys.executable, str(S / s)], check=True)
print("\nAll done! Open dashboard/sales_dashboard.html in your browser.")
