from getgauge.python import step, before_scenario, Messages

vowels = ["a", "e", "i", "o", "u"]


def number_of_vowels(word):
    return len([elem for elem in list(word) if elem in vowels])


# --------------------------
# Gauge step implementations
# --------------------------


@step("<word> の母音の数は <number> であること")
def assert_no_of_vowels_in(word, number):
    assert str(number) == str(number_of_vowels(word))


@step("英語の母音とは <vowels> である")
def assert_default_vowels(given_vowels):
    Messages.write_message("Given vowels are {0}".format(given_vowels))
    assert given_vowels == "".join(vowels)


@step("ほぼすべての単語に母音が含まれること <table>")
def assert_words_vowel_count(table):
    actual = [str(number_of_vowels(word)) for word in table.get_column_values_with_name("Word")]
    expected = [str(count) for count in table.get_column_values_with_name("Vowel Count")]
    assert expected == actual


# ---------------
# Execution Hooks
# ---------------


@before_scenario()
def before_scenario_hook():
    assert "".join(vowels) == "aeiou"
