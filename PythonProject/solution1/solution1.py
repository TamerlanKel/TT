#Необходимо реализовать декоратор @strict Декоратор проверяет соответствие типов аргументов,
# переданных в вызов функции, типам аргументов, объявленным в прототипе функции.
# (подсказка: аннотации типов аргументов можно получить из атрибута объекта функции func.__annotations__
# или с помощью модуля inspect) При несоответствии типов выбрасывать исключение
# TypeError Гарантируется, что параметры в декорируемых функциях будут следующих типов: bool, int, float, str Гарантируется,
# что в декорируемых функциях не будет значений параметров по умолчанию
def strict(func):
    def wrapper(*args, **kwargs):
        annotations = func.__annotations__
        arg_types = list(annotations.values())[:-1] if 'return' in annotations else list(annotations.values())

        for i, (arg, expected_type) in enumerate(zip(args, arg_types)):
            if not isinstance(arg, expected_type):
                arg_name = list(annotations.keys())[i]
                raise TypeError(f"Argument {arg_name} must be of type {expected_type.__name__}, "
                                f"got {type(arg).__name__}")

        for arg_name, arg in kwargs.items():
            expected_type = annotations[arg_name]
            if not isinstance(arg, expected_type):
                raise TypeError(f"Argument {arg_name} must be of type {expected_type.__name__}, "
                                f"got {type(arg).__name__}")

        return func(*args, **kwargs)

    return wrapper


@strict
def sum_two(a: int, b: int) -> int:
    return a + b


print(sum_two(1, 2))  # >>> 3
print(sum_two(1, 2.4))  # >>> TypeError
