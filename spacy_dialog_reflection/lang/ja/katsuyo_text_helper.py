from collections.abc import Callable
from typing import Optional, Union
from spacy_dialog_reflection.lang.ja.katsuyo_text import (
    IKatsuyoTextHelper,
    NonKatsuyoText,
)
import spacy_dialog_reflection.lang.ja.katsuyo as k
import spacy_dialog_reflection.lang.ja.katsuyo_text as kt


# TODO このクラスは、KatsuyoTextBuilder的な名前のクラスに変更する
#      gokan等が必要なく、KatsuyoTextを返すだけのクラスにする
class Ukemi(kt.IKatsuyoTextHelper):
    def __init__(
        self,
        bridge: Optional[
            Callable[[Union[kt.KatsuyoText, kt.NonKatsuyoText]], kt.KatsuyoText]
        ] = None,
    ) -> None:
        if bridge is None:

            def __default(
                pre: Union[kt.KatsuyoText, kt.NonKatsuyoText]
            ) -> kt.KatsuyoText:
                # デフォルトでは動詞「なる」でブリッジ
                naru = kt.KatsuyoText(
                    gokan="な",
                    katsuyo=k.GODAN_RA_GYO,
                )

                if issubclass(
                    type(pre),
                    (kt.NonKatsuyoText),
                ):
                    ni = kt.NonKatsuyoText("に")
                    return pre + ni + naru + kt.Reru()

                if issubclass(
                    type(pre.katsuyo),
                    (k.KeiyoushiKatsuyo, k.KeiyoudoushiKatsuyo),
                ):
                    return pre + naru + kt.Reru()

                raise ValueError(
                    f"Unsupported katsuyo_text in Ukemi: {pre} type: {type(pre)} katsuyo: {type(pre.katsuyo)}"
                )

            bridge = __default

        super().__init__(bridge)

    def try_merge(self, pre: kt.KatsuyoText) -> Optional[kt.KatsuyoText]:
        katsuyo_class = type(pre.katsuyo)
        if issubclass(katsuyo_class, k.DoushiKatsuyo):
            # サ行変格活用のみ特殊
            if issubclass(katsuyo_class, k.SaGyoHenkakuKatsuyo):
                # 用法的に「〜する」は「れる/られる」どちらでもよいため固定
                # 用法的に「〜ずる」は文語が多いため未然形「〜ぜ られる」を採用
                if pre.katsuyo.shushi == "する":
                    return pre + kt.Reru()
                elif pre.katsuyo.shushi == "ずる":
                    return pre + kt.Rareru()

            mizen_text = pre.gokan + pre.katsuyo.mizen
            if mizen_text[-1] in k.DAN["あ"]:
                return pre + kt.Reru()
            else:
                return pre + kt.Rareru()

        return None


class Shieki(IKatsuyoTextHelper):
    def __init__(
        self,
        bridge: Optional[
            Callable[[Union[kt.KatsuyoText, kt.NonKatsuyoText]], kt.KatsuyoText]
        ] = None,
    ) -> None:
        if bridge is None:

            def __default(
                pre: Union[kt.KatsuyoText, kt.NonKatsuyoText]
            ) -> kt.KatsuyoText:
                if issubclass(
                    type(pre),
                    (kt.NonKatsuyoText),
                ):
                    ni = kt.NonKatsuyoText("に")
                    return pre + ni + kt.Saseru()

                if issubclass(
                    type(pre.katsuyo),
                    (k.KeiyoushiKatsuyo, k.KeiyoudoushiKatsuyo),
                ):
                    # 「させる」を動詞として扱い連用形でブリッジ
                    renyo_text = pre.gokan + pre.katsuyo.renyo
                    return NonKatsuyoText(renyo_text) + kt.Saseru()

                raise ValueError(
                    f"Unsupported katsuyo_text in Shieki: {pre} type: {type(pre)} katsuyo: {type(pre.katsuyo)}"
                )

            bridge = __default

        super().__init__(bridge)

    def try_merge(self, pre: kt.KatsuyoText) -> Optional[kt.KatsuyoText]:
        katsuyo_class = type(pre.katsuyo)
        if issubclass(katsuyo_class, k.DoushiKatsuyo):
            # サ行変格活用のみ特殊
            if issubclass(katsuyo_class, k.SaGyoHenkakuKatsuyo):
                # 用法的に「〜する」は「せる/させる」どちらでもよいため固定
                # 用法的に「〜ずる」は「〜じ させる」を採用
                if pre.katsuyo.shushi == "する":
                    return pre + kt.Seru()
                elif pre.katsuyo.shushi == "ずる":
                    return pre + kt.Saseru()

            mizen_text = pre.gokan + pre.katsuyo.mizen
            if mizen_text[-1] in k.DAN["あ"]:
                return pre + kt.Seru()
            else:
                return pre + kt.Saseru()

        return None


# 否定
class Hitei(IKatsuyoTextHelper):
    # 現状、出力文字列としては「ない」のみサポート
    # TODO オプションで「ぬ」を選択できるように

    def __init__(
        self,
        bridge: Optional[
            Callable[[Union[kt.KatsuyoText, kt.NonKatsuyoText]], kt.KatsuyoText]
        ] = None,
    ) -> None:
        if bridge is None:

            def __default(
                pre: Union[kt.KatsuyoText, kt.NonKatsuyoText]
            ) -> kt.KatsuyoText:
                if issubclass(
                    type(pre),
                    (kt.NonKatsuyoText),
                ):
                    # TODO 助詞のハンドリング
                    deha = kt.NonKatsuyoText("では")
                    return pre + deha + kt.Nai()

                if issubclass(
                    type(pre.katsuyo),
                    k.KeiyoushiKatsuyo,
                ):
                    # 「ない」を形容詞として扱い連用形でブリッジ
                    renyo_text = pre.gokan + pre.katsuyo.renyo
                    return NonKatsuyoText(renyo_text) + kt.Nai()
                elif issubclass(
                    type(pre.katsuyo),
                    k.KeiyoudoushiKatsuyo,
                ):
                    # 「ない」を形容詞として扱い連用形でブリッジ
                    # 形容動詞は「ない」には特殊な形式で紐づく
                    renyo_text = pre.gokan + pre.katsuyo.renyo_nai
                    return NonKatsuyoText(renyo_text) + kt.Nai()

                raise ValueError(
                    f"Unsupported katsuyo_text in Hitei: {pre} type: {type(pre)} katsuyo: {type(pre.katsuyo)}"
                )

            bridge = __default

        super().__init__(bridge)

    def try_merge(self, pre: kt.KatsuyoText) -> Optional[kt.KatsuyoText]:
        katsuyo_class = type(pre.katsuyo)
        if issubclass(katsuyo_class, k.DoushiKatsuyo):
            return pre + kt.Nai()

        return None


# # 自分の希望
# class KibouSelf(IKatsuyoTextAppendants):
#     def append(self, katsuyo_text: kt.KatsuyoText) -> kt.KatsuyoText:
#         if katsuyo_text.katsuyo.hinshi == k.KatsuyoHinshi.DOUSHI:
#             renyo_text = katsuyo_text.gokan + katsuyo_text.katsuyo.renyo
#             return kt.KatsuyoText(
#                 gokan=renyo_text + kt.TAI.gokan,
#                 katsuyo=kt.TAI.katsuyo,
#             )
#         # TODO 他のハンドリング
#         return kt.KatsuyoText(
#             gokan="",
#             katsuyo=kt.TAI.katsuyo,
#         )


# # 他人の希望
# class KibouOthers(IKatsuyoTextAppendants):
#     # 現状、出力文字列としては「ない」のみサポート
#     # TODO オプションで「ぬ」を選択できるように

#     def append(self, katsuyo_text: kt.KatsuyoText) -> kt.KatsuyoText:
#         renyo_text = katsuyo_text.gokan + katsuyo_text.katsuyo.renyo
#         return kt.KatsuyoText(
#             gokan=renyo_text + kt.TAGARU.gokan,
#             katsuyo=kt.TAGARU.katsuyo,
#         )
