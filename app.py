import argparse
import sys
from report_tests import ReportTests

def main():
  parser = argparse.ArgumentParser(description="Run usage report tests")

  group = parser.add_mutually_exclusive_group(required=True)
  group.add_argument(
    "--all", "-a",
    action="store_true",
    help="Run all available tests"
  )
  group.add_argument(
    "--select", "-s",
    nargs="+",
    metavar="TEST_LABEL",
    help="Run selected tests by label (space-separated)"
  )

  parser.add_argument(
    "--product", default="ALL", choices=["ALL", "CONTENT", "EMBED"],
    help="Product type to test (default: ALL)"
  )
  parser.add_argument(
    "--env", default="prod", choices=["prod", "stage"],
    help="Environment to test in (default: prod)"
  )
  parser.add_argument(
    "--interface", default="api", choices=["api", "ui"],
    help="Test interface: api or ui (default: api)"
  )

  parser.add_argument(
    "--output", "-o",
    type=str,
    help="Write output to specified file"
  )

  args = parser.parse_args()

  # Handle output redirection
  if args.output:
    sys.stdout = open(args.output, "w")

  usage = ReportTests(
    product=args.product,
    env=args.env,
    interface=args.interface
  )

  if args.all:
    usage.runall()
  else:
    usage._run(args.select)

  if args.output:
    sys.stdout.close()

if __name__ == "__main__":
  main()
