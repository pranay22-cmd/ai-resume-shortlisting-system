def calculate_final_score(
    text_match,
    skill_match,
    semantic_match,
    experience_match
):
    """
    Calculate the final candidate score.

    Weights:
    Text Match: 15%
    Skills Match: 35%
    Semantic AI Match: 35%
    Experience Match: 15%
    """

    final_score = (
        (text_match * 0.15)
        + (skill_match * 0.35)
        + (semantic_match * 0.35)
        + (experience_match * 0.15)
    )

    return round(final_score, 2)


def get_recommendation(final_score):

    if final_score >= 70:
        return "SHORTLISTED", "Strong Match"

    elif final_score >= 50:
        return "MAYBE", "Moderate Match"

    else:
        return "REJECTED", "Poor Match"


if __name__ == "__main__":

    score = calculate_final_score(
        80,
        90,
        85,
        70
    )

    print("Final Score:", score)

    status, recommendation = get_recommendation(score)

    print("Status:", status)
    print("Recommendation:", recommendation)