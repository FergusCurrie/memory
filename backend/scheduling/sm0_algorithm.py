import datetime
import logging
from scheduling_utils import get_consecutive_correct, get_last_review_date

# Set up logging
logger = logging.getLogger(__name__)


def sm0_check_card(card, card_reviews) -> bool:
    if len(card_reviews) == 0:
        return True
    consecutive_correct = get_consecutive_correct(card_reviews)
    interval = 1 * 2 ** (consecutive_correct - 1)
    today = datetime.now().date()
    last_review_date = get_last_review_date(card_reviews)
    next_review_date = last_review_date + datetime.timedelta(days=interval)
    return next_review_date >= today


def sm0_algorithm(cards, reviews):
    cards_to_review = []
    for card in cards:
        card_reviews = [review for review in reviews if review["card_id"] == card["id"]]
        if sm0_check_card(card, card_reviews):
            cards_to_review.append(card)
    return cards_to_review
