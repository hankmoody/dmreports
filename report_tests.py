from report import Report
from report_ui import ReportUI
from copy import deepcopy
from datetime import datetime
from pathlib import Path
import json

class ReportTests:

  def __init__(self, product='ALL', env='prod', interface='api'):
    self.product = product
    self.env = env
    self.interface = interface
    if interface == 'ui':
      self.dmanalyst = ReportUI(env)
    else:
      self.dmanalyst = Report(env)
    self._load_tests()
  
  def _load_tests(self):
    config_path = 'report_tests.json'
    config_file = Path(config_path)
    if not config_file.exists():
      raise FileNotFoundError(f"Test config file not found: {config_path}")
    
    with open(config_file, 'r') as f:
      config = json.load(f)

    self.default_payload = config.get("default_payload", {})
    self.tests = config.get("tests", {})

  def _run_report(self, testconfig, label):
    payload = deepcopy(self.default_payload)
    payload.update(testconfig)
    payload['product'] = self.product
    if self.interface == 'ui':
      payload['name'] = label + ' ' + datetime.now().strftime("%H%M")
    self.dmanalyst.create_report(**payload)
    self.dmanalyst.get_download_links_when_ready()

  def _run(self, selected_labels=None):      
    passed = []
    failed = []
    labels_to_run = selected_labels if selected_labels else self.tests.keys()
    
    for label in labels_to_run:
      if label not in self.tests:
        print(f"[SKIPPED] Unknown test: {label}")
        continue

      print(f"\n========== {label} with PRODUCT={self.product} and ENV={self.env} and INTERFACE={self.interface} ==========")
      try:
        self._run_report(self.tests[label], label)
        print(f"[PASSED] {label}")
        passed.append(label)
      except Exception as e:
        print(f"[FAILED] {label}")
        failed.append((label, str(e)))

    print("\n===================== SUMMARY =====================")
    print(f"\n✅ Passed: {len(passed)}")
    for label in passed:
      print(f"  - {label}")
    print(f"\n❌ Failed: {len(failed)}")
    for label, reason in failed:
      print(f"  - {label}")
    print("\n===================================================")

  def runall(self):
    self._run()