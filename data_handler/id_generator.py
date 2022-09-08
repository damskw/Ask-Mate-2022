import random
import string


def mix(a_list: list) -> list:
    index_order = random.sample(range(len(a_list)), len(a_list))
    next_element = map(lambda index: a_list[index], index_order)
    return list(next_element)


def convert_list_to_string(a_list: list) -> str:
    """

    Args:
        a_list: list - list to be converted

    Returns:
        a_string: str - a string made of the list items joined together

    """
    a_string = "".join(a_list)
    return a_string


def generate_id(
        number_of_small_letters: int,
        number_of_capital_letters: int,
        number_of_digits: int,
        number_of_special_chars: int,
        allowed_special_chars=r"_+-!") -> str:
    id_characters = []
    id_characters.extend(random.choices(string.ascii_lowercase, k=number_of_small_letters))
    id_characters.extend(random.choices(string.ascii_uppercase, k=number_of_capital_letters))
    id_characters.extend(random.choices(string.digits, k=number_of_digits))
    id_characters.extend(random.choices(allowed_special_chars, k=number_of_special_chars))
    id_characters_mixed = mix(id_characters)
    generated_id = convert_list_to_string(id_characters_mixed)
    return generated_id  # eg. 'T!uq6-b4Yq'


def is_id_unique(an_id: str, a_collection: list or tuple) -> bool:
    """
    Evaluates if a given id in string format is unique (is not the same) as other ids from the collection.
    :param an_id: any string representing an id
    :param a_collection: collection of strings (list or tuple of strings)
    :return:
    """
    an_iterator = map(lambda question_id: str(question_id), a_collection)
    return not (an_id in an_iterator)


def generate_unique_id(
        collection: list,
        number_of_small_letters,
        number_of_capital_letters,
        number_of_digits,
        number_of_special_chars,
        allowed_special_chars=r"_+-!") -> str:
    """
    Generate an ID that is unique in the collection of IDs.
    Args:
        collection (object): list - list of IDs
        number_of_small_letters: int - number of lowercase letters that the ID should contain
        number_of_capital_letters: int - number of capital letter that the ID should contain
        number_of_digits: int - number of digits that the ID should contain
        number_of_special_chars: int - number of special characters that the ID should contain
        allowed_special_chars: str - special characters that are allowed to be used in ID
    """
    new_id = generate_id(
        number_of_small_letters,
        number_of_capital_letters,
        number_of_digits,
        number_of_special_chars,
        allowed_special_chars)
    if is_id_unique(new_id, collection):
        return new_id
    return generate_unique_id(
        collection,
        number_of_small_letters,
        number_of_capital_letters,
        number_of_digits,
        number_of_special_chars,
        allowed_special_chars)
