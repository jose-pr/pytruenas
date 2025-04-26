import argparse

parser =argparse.ArgumentParser("PyTrueNAS", "Utility tool to manage and configure TrueNAS systems")
parser.add_argument('--config', '-c', help='Config file to use')

action = parser.add_subparsers(title='action', dest='action', required=True)
runcommand = action.add_parser('run', help='Run Command')
runcommand.add_argument('--steps','-s', help='Select which steps to run')

if __name__ == '__main__':
    args = parser.parse_args()
    print(args)
    