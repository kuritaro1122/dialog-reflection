import pytest
from spacy_dialog_reflection.lang.ja.katsuyo_text import (
    KatsuyoText,
)
from spacy_dialog_reflection.lang.ja.katsuyo import (
    GODAN_BA_GYO,
    GODAN_GA_GYO,
    GODAN_KA_GYO,
    GODAN_MA_GYO,
    GODAN_NA_GYO,
    GODAN_RA_GYO,
    GODAN_SA_GYO,
    GODAN_TA_GYO,
    GODAN_WAA_GYO,
    KEIYOUDOUSHI,
    KEIYOUSHI,
)
from spacy_dialog_reflection.lang.ja.katsuyo_text_appender import Nai, Shieki, Ukemi
from spacy_dialog_reflection.lang.ja.katsuyo_text_builder import SpacyKatsuyoTextBuilder


@pytest.fixture(scope="session")
def spacy_detector():
    return SpacyKatsuyoTextBuilder().root_detector


@pytest.fixture(scope="session")
def spacy_appender_detector():
    return SpacyKatsuyoTextBuilder().appender_detector


@pytest.mark.parametrize(
    "text, root_text, pos, expected",
    [
        (
            "あなたと歩く",
            "歩く",
            "VERB",
            KatsuyoText(
                gokan="歩",
                katsuyo=GODAN_KA_GYO,
            ),
        ),
        (
            "あなたと稼ぐ",
            "稼ぐ",
            "VERB",
            KatsuyoText(
                gokan="稼",
                katsuyo=GODAN_GA_GYO,
            ),
        ),
        (
            "あなたと話す",
            "話す",
            "VERB",
            KatsuyoText(
                gokan="話",
                katsuyo=GODAN_SA_GYO,
            ),
        ),
        (
            "あなたと待つ",
            "待つ",
            "VERB",
            KatsuyoText(
                gokan="待",
                katsuyo=GODAN_TA_GYO,
            ),
        ),
        (
            "あなたと死ぬ",
            "死ぬ",
            "VERB",
            KatsuyoText(
                gokan="死",
                katsuyo=GODAN_NA_GYO,
            ),
        ),
        (
            "あなたと遊ぶ",
            "遊ぶ",
            "VERB",
            KatsuyoText(
                gokan="遊",
                katsuyo=GODAN_BA_GYO,
            ),
        ),
        (
            "本を読む",
            "読む",
            "VERB",
            KatsuyoText(
                gokan="読",
                katsuyo=GODAN_MA_GYO,
            ),
        ),
        (
            "あなたと帰る",
            "帰る",
            "VERB",
            KatsuyoText(
                gokan="帰",
                katsuyo=GODAN_RA_GYO,
            ),
        ),
        (
            "あなたと買う",
            "買う",
            "VERB",
            KatsuyoText(
                gokan="買",
                katsuyo=GODAN_WAA_GYO,
            ),
        ),
        (
            "あなたは美しい",
            "美しい",
            "ADJ",
            KatsuyoText(
                gokan="美し",
                katsuyo=KEIYOUSHI,
            ),
        ),
        (
            "あなたは傲慢だ",
            "傲慢",
            "ADJ",
            KatsuyoText(
                gokan="傲慢",
                katsuyo=KEIYOUDOUSHI,
            ),
        ),
        (
            "それは明日かな",
            "明日",
            "NOUN",
            KatsuyoText(
                gokan="明日",
                katsuyo=KEIYOUDOUSHI,
            ),
        ),
        (
            "それはステファンだ",
            "ステファン",
            "PROPN",
            KatsuyoText(
                gokan="ステファン",
                katsuyo=KEIYOUDOUSHI,
            ),
        ),
    ],
)
def test_spacy_katsuyo_text_detector(
    nlp_ja, spacy_detector, text, root_text, pos, expected
):
    sent = next(nlp_ja(text).sents)
    root_token = sent.root
    assert root_token.text == root_text, "root token is not correct"
    assert root_token.pos_ == pos, "root token is not correct"
    result = spacy_detector.detect(sent)
    assert str(result) == str(expected)


@pytest.mark.parametrize(
    "text, norm, pos, expected",
    [
        (
            "あなたに愛される",
            "れる",
            "AUX",
            [Ukemi],
        ),
        (
            "称号が与えられる",
            "られる",
            "AUX",
            [Ukemi],
        ),
        (
            "あなたを愛させる",
            "せる",
            "AUX",
            [Shieki],
        ),
        (
            "子供を寝させる",
            "させる",
            "AUX",
            [Shieki],
        ),
        (
            "子供を愛さない",
            "ない",
            "AUX",
            [Nai],
        ),
        (
            "子供が寝ない",
            "ない",
            "AUX",
            [Nai],
        ),
        (
            "それは仕方ない",
            "仕方無い",
            "ADJ",
            [],
        ),
        # 現状、Naiとして取れてしまう。言語の返答には
        # 直接的には関係ないので、現状はこのままとする。
        # TODO 「仕方が無い」のような、Naiとして取れるものを取れなくする
        # (
        #     "それは仕方がない",
        #     "無い",
        #     "ADJ",
        #     [],
        # ),
    ],
)
def test_spacy_katsuyo_text_appender_detector(
    nlp_ja, spacy_appender_detector, text, norm, pos, expected
):
    sent = next(nlp_ja(text).sents)
    last_token = sent[-1]
    assert last_token.norm_ == norm, "last token is not correct"
    assert last_token.pos_ == pos, "last token is not correct"
    appenders, has_error = spacy_appender_detector.detect(sent)
    assert not has_error, "has error in detection"
    appender_types = [type(appender) for appender in appenders]
    assert appender_types == expected
