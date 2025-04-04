import sys

def get_rounds():
    if len(sys.argv) == 1:
        return 1  # Default
    elif len(sys.argv) == 2:
        try:
            rounds = int(sys.argv[1])
            if 2 <= rounds <= 5:
                return rounds
        except ValueError:
            pass
    print("Invalid input. Using default (1 round).")
    return 1