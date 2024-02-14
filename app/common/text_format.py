import re


def omit_url(text: str) -> str:
    """URLがある場合省略する

    Parameters
    ----------
    text : str
        変換する文字

    Returns
    -------
    str
        変換後の文字
    """
    pattern = "https?://[\w/:%#\$&\?\(\)~\.=\+\-]+"
    replace_text = "\nユーアールエル省略\n"
    return re.sub(pattern, replace_text, text)


def conv_discord_object(text: str) -> str:
    """_summary_

    Parameters
    ----------
    text : str
        変換する文字

    Returns
    -------
    str
        変換後の文字
    """
    text = re.sub("\<:.+:\d+\>", "サーバー絵文字", text)
    return text
