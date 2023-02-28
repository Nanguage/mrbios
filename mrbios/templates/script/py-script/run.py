from pathlib import Path

import fire


def main(name: str, times: int, out: Path):
    with open(out, 'w') as f:
        for _ in range(times):
            f.write(f"hello {name}")


if __name__ == "__main__":
    fire.Fire(main)
