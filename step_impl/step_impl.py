import subprocess
from subprocess import CompletedProcess
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


@step("<dir_path> ディレクトリを作る")
def assert_mkdir(dir_path):
    result: CompletedProcess = subprocess.run(["mkdir", dir_path], stdout=subprocess.DEVNULL)
    assert 0 == result.returncode


@step("<dir_path> ディレクトリへの移動は <expected> する")
def assert_cd(dir_path, expected):
    result: CompletedProcess = subprocess.run(
        ["cd", dir_path], shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    if expected == "成功":
        assert 0 == result.returncode
    else:
        assert 1 == result.returncode


@step("ディレクトリの中身をリストする")
def assert_ls():
    result: CompletedProcess = subprocess.run(["ls", "-l"], stdout=subprocess.DEVNULL)
    assert 0 == result.returncode


@step("<dir_path> ディレクトリを削除する")
def assert_rm(dir_path):
    result: CompletedProcess = subprocess.run(["rm", "-rf", dir_path], stdout=subprocess.DEVNULL)
    assert 0 == result.returncode


# ---------------
# Execution Hooks
# ---------------


@before_scenario()
def before_scenario_hook():
    assert "".join(vowels) == "aeiou"
