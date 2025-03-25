from utils import get_binary_path, make_executable, run_binary


def test_binray_file():
    # just make sure no exception is raised
    make_executable(get_binary_path("jsteg"))
    out, err = run_binary("jsteg")
    assert out == ""
    assert "Usage: jsteg [command] [args]" in err
