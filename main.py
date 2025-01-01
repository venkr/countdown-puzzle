import time

ops = ["+", "-", "*"]

# Expression type: (operator, number)
ExprType = tuple[str, int]
ExprDict = dict[int, str]


def combine_expr(expr1: ExprType, expr2: ExprType) -> ExprDict:
    result = {}
    for op in ops:
        value = 0
        if op == "+":
            value = expr1[1] + expr2[1]
        elif op == "-":
            value = expr1[1] - expr2[1]
        elif op == "*":
            value = expr1[1] * expr2[1]
        elif op == "/":
            value = expr1[1] / expr2[1]

        if value in result:
            continue

        str = f"({expr1[0]}{op}{expr2[0]})"
        result[value] = str
    return result


def combine_expr_dict(expr1: ExprDict, expr2: ExprDict) -> ExprDict:
    result = {}
    for key1, value1 in expr1.items():
        for key2, value2 in expr2.items():
            for op in ops:
                value = 0
                if op == "+":
                    value = key1 + key2
                elif op == "-":
                    value = key1 - key2
                elif op == "*":
                    value = key1 * key2
                elif op == "/":
                    value = key1 / key2

                if value in result:
                    continue

                str = f"({value1}{op}{value2})"
                result[value] = str
    return result


def pretty_print(expr: ExprDict):
    for key, value in sorted(expr.items()):
        print(f"{key}: {value}")


def pretty_print_txt(expr: ExprDict, filename: str):
    with open(filename, "w") as f:
        for key, value in sorted(expr.items()):
            f.write(f"{key}: {value}\n")


class ExpressionGenerator:
    def __init__(self, min: int, max: int):
        self.min = min
        self.max = max
        self.list = list(range(self.max, self.min - 1, -1))
        self.dict = {str(i): {i: str(i)} for i in self.list}

    def combine(self, length: int) -> list[ExprType]:
        for i in range(len(self.list) - length + 1):
            numbers = self.list[i : i + length]
            number_key = " ".join([str(n) for n in numbers])

            # for a number key eg: 2 3 4 5
            # we must try to combine: (2), (3 4 5)
            # and (2 3), (4 5)
            # and (2 3 4), (5)

            dicts = []
            for j in range(len(numbers) - 1):
                # print(f"combine {numbers[:j+1]} and {numbers[j + 1 :]}")
                dicts.append(
                    combine_expr_dict(
                        self.dict[" ".join([str(n) for n in numbers[: j + 1]])],
                        self.dict[" ".join([str(n) for n in numbers[j + 1 :]])],
                    )
                )

            joined_dict = {}
            for dict in dicts:
                joined_dict.update(dict)

            self.dict[number_key] = joined_dict


def find_missing_numbers(expr: ExprDict, max: int) -> list[int]:
    count = 0
    print("--------------------------------")
    for i in range(1, max + 1):
        if i not in expr:
            print(f"Missing number: {i}")
            count += 1
    print(f"Total missing numbers between 1 and {max}: {count}")


def query_number(expr: ExprDict, number: int):
    if number not in expr:
        print(f"Missing number: {number}")
    else:
        print(f"You can build {number} with {expr[number]}")


# ExpressionGenerator(1, 10).generate()


# pretty_print(combine_expr_dict({3: "(1+2)", -1: "(1-2)", 2: "(1*2)"}, {3: "(3)"}))

eg = ExpressionGenerator(1, 10)
for i in range(2, 11):
    start = time.time()
    eg.combine(i)
    end = time.time()
    print(f"Time taken to build all length {i} expressions: {end - start}")

pretty_print_txt(eg.dict["10 9 8 7 6 5 4 3 2 1"], "output.txt")
find_missing_numbers(eg.dict["10 9 8 7 6 5 4 3 2 1"], 10000)
print("--------------------------------")
query_number(eg.dict["10 9 8 7 6 5 4 3 2 1"], 2024)
query_number(eg.dict["10 9 8 7 6 5 4 3 2 1"], 2025)
query_number(eg.dict["10 9 8 7 6 5 4 3 2 1"], 2026)
query_number(eg.dict["10 9 8 7 6 5 4 3 2 1"], 2027)
query_number(eg.dict["10 9 8 7 6 5 4 3 2 1"], 2028)
