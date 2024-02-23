#!/usr/bin/env python3
import numpy as np
import glob

data_directory = "./vis_project_data/"

# From the thesis:
social_weights = np.array([-1, 0, 1, 2, 2, 3, 5])
cognitive_weights = np.array([-1, 0, 1, 2, 2, 3, 5])


# Types of sessions/files:

types = ["cog", "so"]
whichs = ["base", "inter"]
whatdoors = ["indoor", "outdoor"]

# Combine to single itteratable list
combined = [
    (f, which, whatdoor) for f in types for which in whichs for whatdoor in whatdoors
]

################################################################################


def combined_score(filename, weights):
    """Calculates the 'score' for a single session/file.
    Assumes total session duration is 360s"""
    with open(filename, "r") as file:
        score = 0.0
        total_duration = 0.0
        for count, line in enumerate(file.readlines()):
            # print(count, line)
            data = line.split(",", 4)
            if count == 0:
                continue
            if line[0] == "*":
                break

            t_catagory = int(data[0])
            t_beg = int(data[1])
            t_end = int(data[2])

            assert t_end >= t_beg
            if count == 1:
                assert t_beg == 0

            duration = float(t_end - t_beg) / 360.0
            total_duration += duration
            score += weights[t_catagory - 1] * duration
        # total_duration should be 1
        assert np.abs(total_duration - 1.0) < 1.0e-5
        return score


################################################################################


def print_scores(ca, peer):
    """Calculates the scores for given ca/peer pair.
    It simply prints the result to screen - to be useful, you will want
    to actually store this data (e.g., in a struct or array etc.).
    """

    for type, which, whatdoor in combined:

        weights = cognitive_weights if type == "cog" else social_weights

        # glob creates the list of filenames that match the given pattern
        # '*' is a wildcard
        files = glob.glob(
            data_directory + f"/{type}-*-{which}-*-{ca}-{peer}-{whatdoor}.dtx"
        )

        if len(files) == 0:
            continue

        scores = np.empty([len(files)])
        for i, file in enumerate(files):
            scores[i] = combined_score(file, weights)

        print(f"{type}-{which}-{whatdoor} : {scores.mean():.4f} +/- {scores.std():.4f}")


################################################################################


ca = "barry"
peer = "viola"
print_scores(ca, peer)
