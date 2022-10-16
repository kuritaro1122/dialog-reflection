import pytest
from spacy_dialog_reflection.lang.ja.katsuyo_text import (
    KatsuyoText,
)
from spacy_dialog_reflection.lang.ja.katsuyo import (
    GODAN_BA_GYO,
    GODAN_GA_GYO,
    GODAN_IKU,
    GODAN_KA_GYO,
    GODAN_MA_GYO,
    GODAN_NA_GYO,
    GODAN_RA_GYO,
    GODAN_SA_GYO,
    GODAN_TA_GYO,
    GODAN_WAA_GYO,
    KA_GYO_HENKAKU_KURU,
    KA_GYO_HENKAKU_KURU_KANJI,
    KAMI_ICHIDAN,
    KEIYOUDOUSHI,
    KEIYOUSHI,
    SA_GYO_HENKAKU_SURU,
    SA_GYO_HENKAKU_ZURU,
    SHIMO_ICHIDAN,
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
        # ref, https://ja.wikipedia.org/wiki/五段活用
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
        # 「いく」のみ特殊
        (
            "あなたと行く",
            "行く",
            "VERB",
            KatsuyoText(
                gokan="行",
                katsuyo=GODAN_IKU,
            ),
        ),
        (
            "あなたと往く",
            "往く",
            "VERB",
            KatsuyoText(
                gokan="往",
                katsuyo=GODAN_IKU,
            ),
        ),
        (
            "あなたと逝く",
            "逝く",
            "VERB",
            KatsuyoText(
                gokan="逝",
                katsuyo=GODAN_IKU,
            ),
        ),
        (
            "あなたといく",
            "いく",
            "VERB",
            KatsuyoText(
                gokan="い",
                katsuyo=GODAN_IKU,
            ),
        ),
        (
            "あなたとゆく",
            "ゆく",
            "VERB",
            KatsuyoText(
                # 「ゆく」は「いく」に
                gokan="い",
                katsuyo=GODAN_IKU,
            ),
        ),
        # ref, https://ja.wikipedia.org/wiki/上一段活用
        (
            "あなたと老いる",
            "老いる",
            "VERB",
            KatsuyoText(
                gokan="老い",
                katsuyo=KAMI_ICHIDAN,
            ),
        ),
        (
            "あなたと居る",
            "居る",
            "VERB",
            KatsuyoText(
                gokan="居",
                katsuyo=KAMI_ICHIDAN,
            ),
        ),
        (
            "あなたといる",
            "いる",
            "VERB",
            KatsuyoText(
                gokan="い",
                katsuyo=KAMI_ICHIDAN,
            ),
        ),
        (
            "あなたと起きる",
            "起きる",
            "VERB",
            KatsuyoText(
                gokan="起き",
                katsuyo=KAMI_ICHIDAN,
            ),
        ),
        (
            "あなたと着る",
            "着る",
            "VERB",
            KatsuyoText(
                gokan="着",
                katsuyo=KAMI_ICHIDAN,
            ),
        ),
        (
            "過ぎる",
            "過ぎる",
            "VERB",
            KatsuyoText(
                gokan="過ぎ",
                katsuyo=KAMI_ICHIDAN,
            ),
        ),
        (
            "あなたと閉じる",
            "閉じる",
            "VERB",
            KatsuyoText(
                gokan="閉じ",
                katsuyo=KAMI_ICHIDAN,
            ),
        ),
        (
            "あなたと落ちる",
            "落ちる",
            "VERB",
            KatsuyoText(
                gokan="落ち",
                katsuyo=KAMI_ICHIDAN,
            ),
        ),
        (
            "野菜を煮る",
            "煮る",
            "VERB",
            KatsuyoText(
                gokan="煮",
                katsuyo=KAMI_ICHIDAN,
            ),
        ),
        (
            "日差しを浴びる",
            "浴びる",
            "VERB",
            KatsuyoText(
                gokan="浴び",
                katsuyo=KAMI_ICHIDAN,
            ),
        ),
        (
            "目に染みる",
            "染みる",
            "VERB",
            KatsuyoText(
                gokan="染み",
                katsuyo=KAMI_ICHIDAN,
            ),
        ),
        (
            "目を見る",
            "見る",
            "VERB",
            KatsuyoText(
                gokan="見",
                katsuyo=KAMI_ICHIDAN,
            ),
        ),
        (
            "下に降りる",
            "降りる",
            "VERB",
            KatsuyoText(
                gokan="降り",
                katsuyo=KAMI_ICHIDAN,
            ),
        ),
        # ref, https://ja.wikipedia.org/wiki/下一段活用
        (
            "下に見える",
            "見える",
            "VERB",
            KatsuyoText(
                gokan="見え",
                katsuyo=SHIMO_ICHIDAN,
            ),
        ),
        (
            "報酬を得る",
            "得る",
            "VERB",
            KatsuyoText(
                gokan="得",
                katsuyo=SHIMO_ICHIDAN,
            ),
        ),
        (
            "罰を受ける",
            "受ける",
            "VERB",
            KatsuyoText(
                gokan="受け",
                katsuyo=SHIMO_ICHIDAN,
            ),
        ),
        (
            "宣告を告げる",
            "告げる",
            "VERB",
            KatsuyoText(
                gokan="告げ",
                katsuyo=SHIMO_ICHIDAN,
            ),
        ),
        (
            "映像を見せる",
            "見せる",
            "VERB",
            KatsuyoText(
                gokan="見せ",
                katsuyo=SHIMO_ICHIDAN,
            ),
        ),
        (
            "小麦粉を混ぜる",
            "混ぜる",
            "VERB",
            KatsuyoText(
                gokan="混ぜ",
                katsuyo=SHIMO_ICHIDAN,
            ),
        ),
        (
            "小麦粉を捨てる",
            "捨てる",
            "VERB",
            KatsuyoText(
                gokan="捨て",
                katsuyo=SHIMO_ICHIDAN,
            ),
        ),
        (
            "うどんを茹でる",
            "茹でる",
            "VERB",
            KatsuyoText(
                gokan="茹で",
                katsuyo=SHIMO_ICHIDAN,
            ),
        ),
        (
            "出汁が出る",
            "出る",
            "VERB",
            KatsuyoText(
                gokan="出",
                katsuyo=SHIMO_ICHIDAN,
            ),
        ),
        (
            "親戚を尋ねる",
            "尋ねる",
            "VERB",
            KatsuyoText(
                gokan="尋ね",
                katsuyo=SHIMO_ICHIDAN,
            ),
        ),
        (
            "すぐに寝る",
            "寝る",
            "VERB",
            KatsuyoText(
                gokan="寝",
                katsuyo=SHIMO_ICHIDAN,
            ),
        ),
        (
            "時を経る",
            "経る",
            "VERB",
            KatsuyoText(
                gokan="経",
                katsuyo=SHIMO_ICHIDAN,
            ),
        ),
        (
            "ご飯を食べる",
            "食べる",
            "VERB",
            KatsuyoText(
                gokan="食べ",
                katsuyo=SHIMO_ICHIDAN,
            ),
        ),
        (
            "ご飯を求める",
            "求める",
            "VERB",
            KatsuyoText(
                gokan="求め",
                katsuyo=SHIMO_ICHIDAN,
            ),
        ),
        (
            "麺を入れる",
            "入れる",
            "VERB",
            KatsuyoText(
                gokan="入れ",
                katsuyo=SHIMO_ICHIDAN,
            ),
        ),
        # ref. https://ja.wikipedia.org/wiki/カ行変格活用
        (
            "家にくる",
            "くる",
            "VERB",
            KatsuyoText(
                gokan="",
                katsuyo=KA_GYO_HENKAKU_KURU,
            ),
        ),
        (
            "家に来る",
            "来る",
            "VERB",
            KatsuyoText(
                gokan="来",
                katsuyo=KA_GYO_HENKAKU_KURU_KANJI,
            ),
        ),
        # ref. https://ja.wikipedia.org/wiki/サ行変格活用
        (
            "軽くウォーキングする",
            "ウォーキング",
            "VERB",
            KatsuyoText(
                gokan="ウォーキング",
                katsuyo=SA_GYO_HENKAKU_SURU,
            ),
        ),
        (
            "フライパンを熱する",
            "熱する",
            "VERB",
            KatsuyoText(
                gokan="熱",
                katsuyo=SA_GYO_HENKAKU_SURU,
            ),
        ),
        (
            "影響が生ずる",
            "生ずる",
            "VERB",
            KatsuyoText(
                gokan="生",
                katsuyo=SA_GYO_HENKAKU_ZURU,
            ),
        ),
        # サ行変格活用と間違える可能性がある動詞
        (
            "ひざをずる",
            "ずる",
            "VERB",
            KatsuyoText(
                gokan="ず",
                katsuyo=GODAN_RA_GYO,
            ),
        ),
        (
            "ひざを擦る",
            "擦る",
            "VERB",
            KatsuyoText(
                gokan="擦",
                katsuyo=GODAN_RA_GYO,
            ),
        ),
        # この活用判別は困難なため、現状は未対応
        # (
        #     "ひざをする",
        #     "する",
        #     "VERB",
        #     KatsuyoText(
        #         gokan="す",
        #         katsuyo=GODAN_RA_GYO,
        #     ),
        # ),
        # 形容詞
        (
            "あなたは美しい",
            "美しい",
            "ADJ",
            KatsuyoText(
                gokan="美し",
                katsuyo=KEIYOUSHI,
            ),
        ),
        # 形容動詞
        (
            "あなたは傲慢だ",
            "傲慢",
            "ADJ",
            KatsuyoText(
                gokan="傲慢",
                katsuyo=KEIYOUDOUSHI,
            ),
        ),
        # 名詞
        (
            "それは明日かな",
            "明日",
            "NOUN",
            KatsuyoText(
                gokan="明日",
                katsuyo=KEIYOUDOUSHI,
            ),
        ),
        # 固有名詞
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
    assert result == expected


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
        # TODO 「仕方が無い」のような、Naiとして取れるものと否定の意を区別する
        (
            "それは仕方がない",
            "無い",
            "ADJ",
            [Nai],
        ),
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
