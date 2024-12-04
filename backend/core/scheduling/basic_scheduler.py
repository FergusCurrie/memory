import logging
from .scheduling_utils import get_consecutive_correct, get_last_review_date
from datetime import datetime, timedelta

# Set up logging
logger = logging.getLogger(__name__)


def get_todays_reviews(cards, reviews):
    cards_to_review = []
    today = datetime.now().date()

    for card in cards:
        logger.info(f"Processing card: {card}")
        card_reviews = [review for review in reviews if review["card_id"] == card["id"]]
        logger.info(f"Card reviews: {card_reviews}")
        if not card_reviews:
            cards_to_review.append(card)
            logger.info(f"Card {card} added to review")
        else:
            consecutive_correct = get_consecutive_correct(card_reviews)

            logger.info(f"Consecutive correct: {consecutive_correct}")

            last_review_date = datetime.strptime(get_last_review_date(card_reviews), "%Y-%m-%d %H:%M:%S").date()

            logger.info(f"Last review date: {last_review_date}")

            if consecutive_correct == 0:
                interval = 1
            elif consecutive_correct == 1:
                interval = 3
            else:
                previous_review_date = get_last_review_date(card_reviews)
                interval = ((last_review_date - previous_review_date).days * 2.5) + 1

            logger.info(f"Interval: {interval}")

            interval = min(int(interval), 365)
            next_review_date = last_review_date + timedelta(days=interval)

            if next_review_date <= today:
                cards_to_review.append(card)

    return cards_to_review
