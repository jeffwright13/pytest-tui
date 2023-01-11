import random
import warnings

import faker


def fake_data(min: int = 30, max: int = 120) -> str:
    return faker.Faker().text(random.randint(min, max))


def test_1_fails_with_warnings():
    print("This test fails with warnings. See Warnings section for info.")
    warnings.warn(Warning(fake_data(50, 200)))
    warnings.warn(UserWarning(fake_data(55, 205)))
    warnings.warn(DeprecationWarning(fake_data(55, 205)))
    warnings.warn(SyntaxWarning(fake_data(55, 205)))
    warnings.warn(RuntimeWarning(fake_data(55, 205)))
    warnings.warn(FutureWarning(fake_data(55, 205)))
    warnings.warn(PendingDeprecationWarning(fake_data(55, 205)))
    warnings.warn(ImportWarning(fake_data(55, 205)))
    warnings.warn(UnicodeWarning(fake_data(55, 205)))
    warnings.warn(BytesWarning(fake_data(55, 205)))
    warnings.warn(ResourceWarning(fake_data(55, 205)))
    warnings.warn((fake_data(55, 205)))
    assert False


def test_2_passes_with_warnings():
    print("This test passes, but with warnings. See Warnings section for info.")
    warnings.warn(Warning(fake_data(50, 200)))
    warnings.warn(UserWarning(fake_data(55, 205)))
    warnings.warn(DeprecationWarning(fake_data(55, 205)))
    warnings.warn(SyntaxWarning(fake_data(55, 205)))
    warnings.warn(RuntimeWarning(fake_data(55, 205)))
    warnings.warn(FutureWarning(fake_data(55, 205)))
    warnings.warn(PendingDeprecationWarning(fake_data(55, 205)))
    warnings.warn(ImportWarning(fake_data(55, 205)))
    warnings.warn(UnicodeWarning(fake_data(55, 205)))
    warnings.warn(BytesWarning(fake_data(55, 205)))
    warnings.warn(ResourceWarning(fake_data(55, 205)))
    warnings.warn((fake_data(55, 205)))
    assert True
