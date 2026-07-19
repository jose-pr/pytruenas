"""Package-level exports: __version__ and public names."""

import pytruenas


def test_version_exposed_and_matches_metadata():
    from importlib.metadata import version

    assert isinstance(pytruenas.__version__, str)
    assert pytruenas.__version__ == version("pytruenas")


def test_public_api_importable():
    from pytruenas import TrueNASClient, Namespace, Credentials  # noqa: F401

    for name in ("TrueNASClient", "Namespace", "Credentials", "__version__"):
        assert name in pytruenas.__all__
