import argparse
from lib.v2.fish_tank import FishTank
from lib.v2.beta_fish import BetaFish

def parse_args():
    parser = argparse.ArgumentParser(description="Run the FishTank simulation.")
    parser.add_argument("--width", type=int, default=800, help="Width of the fish tank window")
    parser.add_argument("--height", type=int, default=600, help="Height of the fish tank window")
    parser.add_argument("--fps", type=int, default=60, help="Frames per second")
    return parser.parse_args()

def main():
    args = parse_args()
    fish_tank = FishTank(width=args.width, height=args.height, fps=args.fps)
    fish_tank.run()

if __name__ == "__main__":
    main()
