import MeCab
from config.mecab import MECAB_USER_DICT

USER_DICT = r'-u"' + str(MECAB_USER_DICT) + '"'
FORMAT = r' -F"%M\\t%c,%H\\n"'


def get_pronunciation(text: str) -> str:
    """読みを取得する

    Parameters
    ----------
    text : str
        対象文字列

    Returns
    -------
    str
        読み
    """

    # MeCabを使用しない場合は何もしない
    if MECAB_USER_DICT is None:
        return text

    mecab = MeCab.Tagger(" ".join([USER_DICT, FORMAT]))
    m_result = mecab.parse(text).splitlines()
    m_result = m_result[:-1]  # 最後の1行は不要な行なので除く

    pronunciation = ""
    for line in m_result:
        if "\t" not in line:
            continue

        surface, feature = line.split("\t")
        features = feature.split(",")

        if is_converting_target(features):
            pronunciation += features[-1]
        else:
            pronunciation += surface

    return pronunciation


def is_converting_target(features: list) -> bool:
    """変換対象かどうか

    Parameters
    ----------
    features : list
        MeCabから帰ってくる情報

    Returns
    -------
    bool
        結果
    """
    # 発音が設定されていないものはスルー
    if features[-1] == "*":
        return False

    # 絵文字などは変換
    if features[1] == "記号" and features[2] == "一般":
        return True

    # 固有名詞は変換
    if features[1] == "名詞" and features[2] == "固有名詞":
        return True

    # 上記以外はスルー
    return False
