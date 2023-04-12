import nox

# nox.options.sessions = ["install_requirements", "install_requirements_plus_package", "install_requirements_dev", "install_requirements_dev_plus_package", "test_with_pytest", "tests"]

nox.options.sessions = [
    "install_requirements",
    "install_requirements_plus_package",
    "install_requirements_dev",
    "install_requirements_dev_plus_package",
    "test_with_pytest",
    "test_with_selenium_base",
    "test_with_pytest_tui_logfold",
    "test_with_pytest_tui_regexfold",
    "test_with_selenium_bas_logfold",
    "test_with_selenium_bas_regexfold",
]


@nox.session(python=["3.8", "3.9", "3.10", "3.11"], tags=["install", "basic"])
def install_requirements_user(session):
    session.install("-r", "requirements/requirements.txt")


@nox.session(python=["3.8", "3.9", "3.10", "3.11"], tags=["install"])
def install_requirements_user_plus_pytest_tui_package(session):
    install_requirements_user(session)
    session.install(".")


@nox.session(python=["3.8", "3.9", "3.10", "3.11"], tags=["install", "dev"])
def install_requirements_dev(session):
    session.install("-r", "requirements/requirements-dev.txt")


@nox.session(python=["3.8", "3.9", "3.10", "3.11"], tags=["install", "dev"])
def install_requirements_dev_plus_pytest_tui_package(session):
    install_requirements_dev(session)
    session.install(".")


@nox.session(python=["3.8", "3.9", "3.10", "3.11"], tags=["tui"])
def test_with_pytest_tui(session):
    session.install("-r", "requirements/requirements-dev.txt")
    session.install(".")
    session.run("pytest", "demo-tests/", "--tui")


@nox.session(python=["3.8", "3.9", "3.10", "3.11"], tags=["tui", "fold", "log"])
def test_with_pytest_tui_logfold(session):
    install_requirements_dev_plus_pytest_tui_package(session)
    session.run("pytest", "demo-tests/", "--tui", "tui-fold-level=debug")


@nox.session(python=["3.8", "3.9", "3.10", "3.11"], tags=["tui", "fold", "log"])
def test_with_selenium_base_logfold(session):
    test_with_pytest_tui_logfold(session)
    session.install("--upgrade", "-Iv", "rich==13.3.0")
    session.install("selenium-base")
    session.run("pytest", "testing/sb")


@nox.session(python=["3.8", "3.9", "3.10", "3.11"], tags=["tui", "fold", "regex"])
def test_with_pytest_tui_regexfold(session):
    install_requirements_dev_plus_pytest_tui_package(session)
    session.run("pytest", "demo-tests/", "--tui", "tui-fold-regex=​​​;￼​")  # ZWS & ZWJ


@nox.session(python=["3.8", "3.9", "3.10", "3.11"], tags=["tui", "fold", "regex"])
def test_with_selenium_base_regexfold(session):
    test_with_pytest_tui_regexfold(session)
    session.install("--upgrade", "-Iv", "rich==13.3.0")
    session.install("selenium-base")
    session.run("pytest", "testing/sb")
