def test_true_assertion(pytester):
    pytester.makepyfile(
        """
        def test_foo():
            assert True
    """
    )
    result = pytester.runpytest()
    result.assert_outcomes(failed=0, passed=1)


def test_false_assertion(testdir):
    testdir.makepyfile(
        """
        def test_foo():
            assert False
    """
    )
    result = testdir.runpytest()
    result.assert_outcomes(failed=1, passed=0)
