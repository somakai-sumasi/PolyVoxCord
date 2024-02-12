import MeCab
import os

USER_DICT=r'-u"'+os.getenv("MECAB_USER_DICT")+'"'
FORMAT=r' -F"%M\\t%c,%H\\n"'


def get_pronunciation(text):
    mecab = MeCab.Tagger(' '.join([USER_DICT, FORMAT]))
    m_result = mecab.parse(text).splitlines()
    m_result = m_result[:-1] #最後の1行は不要な行なので除く

    pronunciation = ''
    for line in m_result:
        if '\t' not in line: continue

        surface, feature = line.split('\t')
        features = feature.split(',')

        if(is_converting_target(features)):
            pronunciation += features[-1]
        else:
            pronunciation += surface

    return pronunciation

def is_converting_target(features):
    # 発音が設定されていないものはスルー
    if features[-1] == '*':
        return False

    # 絵文字などは変換
    if features[1] == '記号' and  features[2] == '一般':
        return True

    # 固有名詞は変換
    if features[1] == '名詞' and  features[2] == '固有名詞':
        return True

    # 上記以外はスルー
    return False
