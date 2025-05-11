import argparse
from text.version import update_version

def main():
    parser = argparse.ArgumentParser(description='Update ZeeText version')
    parser.add_argument('--major', type=int, help='Major version number')
    parser.add_argument('--minor', type=int, help='Minor version number')
    parser.add_argument('--patch', type=int, help='Patch version number')
    parser.add_argument('--build', type=int, help='Build version number')
    
    args = parser.parse_args()
    new_version = update_version(
        major=args.major,
        minor=args.minor,
        patch=args.patch,
        build=args.build
    )
    print(f"Version updated to: {new_version}")

if __name__ == "__main__":
    main()