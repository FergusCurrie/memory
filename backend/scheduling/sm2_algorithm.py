import logging
import traceback
from .scheduling_utils import get_last_review_date
from datetime import datetime, timedelta

# Set up logging
logger = logging.getLogger(__name__)


def sm2_check_card(card, card_reviews) -> bool:
    logger.debug(f"Checking card {card}, has reviews: {card_reviews}")
    if len(card_reviews) == 0:
        return True
    sorted_reviews = sorted(card_reviews, key=lambda x: datetime.strptime(x["date"], "%Y-%m-%d %H:%M:%S"))
    ease_factor = 2.5
    n = 0
    for review in sorted_reviews:
        rating = 4 if review["result"] else 2
        if review["result"]:
            # Correct
            if n == 0:
                interval = 1
            elif n == 1:
                interval = 6
            else:
                interval = int(ease_factor * interval)
        else:
            # Mistake
            n = 0
            interval = 1

        # Update ease factor
        ease_factor = ease_factor + (0.1 - (5 - rating) * (0.08 + (5 - rating) * 0.02))
        if ease_factor < 1.3:
            ease_factor = 1.3

    logger.debug(f"Found interval = {interval}, ease_factor = {ease_factor}")

    today = datetime.now().date()
    last_review_date = get_last_review_date(card_reviews)
    next_review_date = last_review_date + timedelta(days=interval)
    logger.debug(f"Today = {today}, last_review={last_review_date}, next_Review={next_review_date}")
    return next_review_date <= today


def sm2_algorithm(cards, reviews):
    logger.info("Running sm2 algo")
    try:
        cards_to_review = []
        for card in cards:
            card_reviews = [review for review in reviews if review["card_id"] == card["id"]]
            if sm2_check_card(card, card_reviews):
                cards_to_review.append(card)
        return cards_to_review
    except Exception:
        logger.error(f"An error occurred in sm2_algorithm:\n{traceback.format_exc()}")
