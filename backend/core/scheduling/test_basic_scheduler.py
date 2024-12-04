import pytest
from basic_scheduler import get_todays_reviews
from datetime import datetime, timedelta


# Helper function to create a card
def create_card(id, question, answer):
    return {"id": id, "question": question, "answer": answer}


# Helper function to create a review
def create_review(card_id, date, result):
    return {"card_id": card_id, "date": date.strftime("%Y-%m-%d %H:%M:%S"), "result": result}


@pytest.fixture
def sample_cards():
    return [
        create_card(1, "What is the capital of France?", "Paris"),
        create_card(2, "What is 2+2?", "4"),
        create_card(3, "Who wrote Romeo and Juliet?", "William Shakespeare"),
    ]


def test_new_card_should_be_reviewed():
    cards = [create_card(1, "New card", "Answer")]
    reviews = []

    result = get_todays_reviews(cards, reviews)

    assert len(result) == 1
    assert result[0]["id"] == 1


def test_card_reviewed_today_should_not_be_reviewed_again():
    cards = [create_card(1, "Card", "Answer")]
    reviews = [create_review(1, datetime.now(), True)]

    result = get_todays_reviews(cards, reviews)

    assert len(result) == 0


def test_card_reviewed_yesterday_incorrectly_should_be_reviewed_today():
    cards = [create_card(1, "Card", "Answer")]
    reviews = [create_review(1, datetime.now() - timedelta(days=1), False)]

    result = get_todays_reviews(cards, reviews)

    assert len(result) == 1
    assert result[0]["id"] == 1


def test_card_reviewed_correctly_once_should_be_reviewed_after_6_days():
    cards = [create_card(1, "Card", "Answer")]
    reviews = [create_review(1, datetime.now() - timedelta(days=5), True)]

    result = get_todays_reviews(cards, reviews)
    assert len(result) == 0

    reviews = [create_review(1, datetime.now() - timedelta(days=6), True)]
    result = get_todays_reviews(cards, reviews)
    assert len(result) == 1
    assert result[0]["id"] == 1


def test_multiple_cards_with_mixed_review_history(sample_cards):
    reviews = [
        create_review(1, datetime.now() - timedelta(days=1), False),  # Should be reviewed
        create_review(2, datetime.now() - timedelta(days=5), True),  # Should not be reviewed
        create_review(3, datetime.now() - timedelta(days=7), True),  # Should be reviewed
    ]

    result = get_todays_reviews(sample_cards, reviews)
    assert len(result) == 2
    assert set(card["id"] for card in result) == {1, 3}


def test_card_with_long_interval_respects_max_interval():
    cards = [create_card(1, "Card", "Answer")]
    reviews = [
        create_review(1, datetime.now() - timedelta(days=500), True),
        create_review(1, datetime.now() - timedelta(days=400), True),
    ]

    result = get_todays_reviews(cards, reviews)
    assert len(result) == 1
    assert result[0]["id"] == 1
