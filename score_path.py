import os
from sugar3.activity.activity import get_activity_root


def score_path():
    score_path = os.path.join(get_activity_root(), 'data', 'score.pkl')
    return score_path
