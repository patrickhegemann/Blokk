#!/usr/bin/env python

# import cProfile as profile
from tetris.gamestate import GameManager


def main():
    GameManager.instance().start()


if __name__ == "__main__":
    # profile.run('main()')
    main()
