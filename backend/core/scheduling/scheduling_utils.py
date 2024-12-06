def get_consecutive_correct(reviews):
    sorted_reviews = sorted(reviews, key=lambda x: x["date_created"], reverse=True)
    consecutive_correct = 0
    for review in reviews:
        if review["result"]:
            consecutive_correct += 1
        else:
            break
    return consecutive_correct


def get_last_review_date(reviews):
    sorted_reviews = sorted(reviews, key=lambda x: x["date_created"], reverse=True)
    return sorted_reviews[0]["date_created"]
