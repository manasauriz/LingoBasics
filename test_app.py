from project import setup_items, setup_langs
from project import formatted_list, translate_word


def test_setup_items():
    """
    Tests setup_item function of project.py
    """
    items = setup_items("../project/test_assets")
    assert type(items) == dict
    assert len(items) == 2

    assert len(items["animals"]) == 2
    assert ("cat" in items["animals"]) == True
    assert ("dog" in items["animals"]) == True

    assert len(items["body"]) == 2
    assert ("arm" in items["body"]) == True
    assert ("face" in items["body"]) == True


def test_setup_langs():
    """
    Tests setup_langs function of project.py
    """
    langs = setup_langs()
    assert len(langs) == 84

    assert ("german" in langs.values()) == True
    assert ("spanish" in langs.values()) == True

    assert ("english" in langs.values()) == False
    assert ("hindi" in langs.values()) == False


def test_formatted_list():
    """
    Tests formatted_list function of project.py
    """
    original = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    formatted_with_4 = [[1, 2, 3, 4], [5, 6, 7, 8], [9]]
    formatted_with_3 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    formatted_with_2 = [[1, 2], [3, 4], [5, 6], [7, 8], [9]]

    assert formatted_list(original, 4) == formatted_with_4
    assert formatted_list(original, 3) == formatted_with_3
    assert formatted_list(original, 2) == formatted_with_2


def test_translate_word():
    """
    Tests translate_word function of project.py
    """
    assert translate_word("cat", "german") == "Katze"
    assert translate_word("cat", "russian") == "кот"
    assert translate_word("cat", "gibberish") == None
