import pytest

old_version = True


# test_example.py
def one_more(x):
    return x + 1

# @pytest.mark.parametrize(
#     ['input_arg', 'expected_result'],  # Названия аргументов, передаваемых в тест.
#     [(4, 5), (3, 5)],  # Список кортежей со значениями аргументов.
#     ids=['First parameter', 'Second parameter',]
# )
@pytest.mark.parametrize(
    'input_arg, expected_result',
    [
        (4, 5), 
        pytest.param(3, 5, marks=pytest.mark.xfail)  # Ожидается падение теста.
    ],
    ids=['First parameter', 'Second parameter',]
)
def test_one_more(input_arg, expected_result):  # Те же параметры, что и в декораторе.
    assert one_more(input_arg) == expected_result


def get_sort_list(str):
    new_list = sorted(str.split(', '))
    return new_list


def test_sort():
    """Тестируем функцию get_sort_list()."""
    result = get_sort_list('Яша, Саша, Маша, Даша')
    assert result == ['Даша', 'Маша', 'Саша', 'Яша']


def test_type():
    """Тестируем тип данных, возвращаемых из get_sort_list()."""
    result = get_sort_list('Яша, Саша, Маша, Даша')
    # Провальный тест:
    # ожидаем число, но вернётся список.
    assert isinstance(result, int)


@pytest.mark.skipif(
    "sys.version_info > (2, 7)",
    reason='Только для старых версий Python'
)
def test_for_old_versions():
    assert old_version == True


@pytest.mark.xfail(reason='Пусть пока падает, завтра починю.')
def test_false():
    assert False


@pytest.mark.xfail("sys.version_info < (2, 1)", 
                   reason='Это старая версия Python, чего же вы ждали!')
def test_for_new_python():
    assert old_version == True