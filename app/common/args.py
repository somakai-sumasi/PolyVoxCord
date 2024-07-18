import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--guild", type=int, help="ギルドID", required=False)

args = parser.parse_args()
