import pytest
from spacy_dialog_reflection.lang.ja.katsuyo_text import (
    KatsuyoText,
)
from spacy_dialog_reflection.lang.ja.katsuyo import (
    GODAN_BA_GYO,
    KA_GYO_HENKAKU_KURU,
    RARERU,
    RERU,
)
from spacy_dialog_reflection.lang.ja.katsuyo_text_appender import (
    IKatsuyoTextAppender,
    Ukemi,
)
from spacy_dialog_reflection.lang.ja.katsuyo_text_builder import (
    IKatsuyoTextBuilder,
)


@pytest.fixture(scope="session")
def append_multiple():
    class DummyAppender(IKatsuyoTextBuilder):
        def detect_appender(self, _):
            raise NotImplementedError()

        def detect_root(self, _):
            raise NotImplementedError()

    return DummyAppender().append_multiple


@pytest.mark.parametrize(
    "katsuyo_text, expected",
    [
        # TODO もっとテストケースを増やす
        (
            KatsuyoText(
                gokan="",
                katsuyo=KA_GYO_HENKAKU_KURU,
            ),
            KatsuyoText(
                gokan="こ",
                katsuyo=RARERU,
            ),
        ),
        (
            KatsuyoText(
                gokan="遊",
                katsuyo=GODAN_BA_GYO,
            ),
            KatsuyoText(
                gokan="遊ば",
                katsuyo=RERU,
            ),
        ),
    ],
)
def test_zohdoushi_appender_ukemi(katsuyo_text, expected):
    zohdoushi_appender = Ukemi()
    result = zohdoushi_appender.append(katsuyo_text)
    assert str(result) == str(expected)


@pytest.mark.filterwarnings("ignore:ValueError")
@pytest.mark.filterwarnings("ignore:Invalid appender")
def test_katsuyo_text_warning_value_error(append_multiple):
    class AppenderRaiseValueError(IKatsuyoTextAppender):
        def append(self, _):
            raise ValueError("HOGE")

    katsuyo_text = KatsuyoText(
        gokan="",
        katsuyo=KA_GYO_HENKAKU_KURU,
    )
    katsuyo_text_appenders = [
        AppenderRaiseValueError(),
    ]
    result, has_error = append_multiple(
        katsuyo_text,
        katsuyo_text_appenders,
    )
    assert result == katsuyo_text, "No changes"
    assert has_error, "has_error is True"


@pytest.mark.filterwarnings("ignore:None value TypeError Detected")
@pytest.mark.filterwarnings("ignore:Invalid appender")
def test_katsuyo_text_warning_none_type_error(append_multiple):
    class AppenderRaiseTypeError(IKatsuyoTextAppender):
        def append(self, _):
            return KatsuyoText(
                # raise TypeError
                gokan="あ" + None,
                katsuyo=KA_GYO_HENKAKU_KURU,
            )

    katsuyo_text = KatsuyoText(
        gokan="",
        katsuyo=KA_GYO_HENKAKU_KURU,
    )
    katsuyo_text_appenders = [
        AppenderRaiseTypeError(),
    ]
    result, has_error = append_multiple(
        katsuyo_text,
        katsuyo_text_appenders,
    )
    assert result == katsuyo_text, "No changes"
    assert has_error, "has_error is True"
