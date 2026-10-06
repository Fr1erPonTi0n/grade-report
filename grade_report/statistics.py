from collections import defaultdict


def calculate_statistics(students: list[dict]) -> dict:
    if not students:
        return {
            "student_count": 0,
            "average_score": 0.0,
            "minimum_score": None,
            "maximum_score": None,
            "groups": {},
        }

    scores = [student["score"] for student in students]

    group_scores = defaultdict(list)

    for student in students:
        group_scores[student["group"]].append(student["score"])

    groups = {
        group: round(sum(scores_list) / len(scores_list), 2)
        for group, scores_list in sorted(group_scores.items())
    }

    return {
        "student_count": len(students),
        "average_score": round(sum(scores) / len(scores), 2),
        "minimum_score": min(scores),
        "maximum_score": max(scores),
        "groups": groups,
    }
