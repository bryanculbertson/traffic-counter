from click.testing import CliRunner

from traffic_counter.cli import version


def test_version() -> None:
    runner = CliRunner()
    result = runner.invoke(version)
    assert result.exit_code == 0
    assert result.output == "0.1.0\n"
