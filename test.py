import currency_converter


def test_edge_cases():
    assert(currency_converter.main(10, 'SVK', None) is None)
    assert(currency_converter.main(10, 'EUR', 'SVK') is None)
    assert(currency_converter.main(10, None, None) is None)
    assert(currency_converter.main(10, None, 'EUR') is None)
    assert(currency_converter.main(10, 'EUR', None) is not None)
    assert(currency_converter.main(10, 'EUR', 'EUR') is not None)
    assert(currency_converter.main(10, '£', '£') is not None)


def test_all_codes():
    for key, value in sorted(currency_converter.symbol_to_currency_code.items()):
        for key2, value2 in sorted(currency_converter.symbol_to_currency_code.items()):
            for j in value:
                for i in value2:
                    assert(currency_converter.main(10, i, j) is not None)


def test_all_symbols():
    for key, value in sorted(currency_converter.symbol_to_currency_code.items()):
        for key2, value2 in sorted(currency_converter.symbol_to_currency_code.items()):
            assert(currency_converter.main(10, key, key2) is not None)


def main():
    test_edge_cases()
    print("Test edge cases - OK")
    test_all_codes()
    print("Test all codes - OK")
    test_all_symbols()
    print("Test all symbols - OK")
    print("All tests passed")


if __name__ == "__main__":
    main()