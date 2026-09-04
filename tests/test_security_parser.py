from security_analyzer.parser import AgentParser


def test_parse_python_file(tmp_path):
    agent_file = tmp_path / "agent.py"
    agent_file.write_text("""
import os
import subprocess


def hello():
    return "hello"


class Agent:
    pass
""")

    agent = AgentParser().parse(str(agent_file))

    assert len(agent.files) == 1

    parsed_file = agent.files[0]

    assert parsed_file.language == "python"
    assert "os" in parsed_file.imports
    assert "subprocess" in parsed_file.imports
    assert "hello" in parsed_file.functions
    assert "Agent" in parsed_file.classes


def test_detects_tool_calls(tmp_path):
    agent_file = tmp_path / "agent.py"
    agent_file.write_text("""
import subprocess


def run_command():
    subprocess.run("ls")
    os.system("whoami")
""")

    agent = AgentParser().parse(str(agent_file))

    parsed_file = agent.files[0]

    assert "subprocess.run" in parsed_file.tool_calls
    assert "os.system" in parsed_file.tool_calls


def test_detects_async_functions(tmp_path):
    agent_file = tmp_path / "agent.py"
    agent_file.write_text("""
async def fetch_data():
    return "data"
""")

    agent = AgentParser().parse(str(agent_file))

    assert "fetch_data" in agent.files[0].functions


def test_detects_dependencies(tmp_path):
    requirements = tmp_path / "requirements.txt"
    requirements.write_text("requests\n")

    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text("[project]\nname = 'test-agent'\n")

    agent_file = tmp_path / "agent.py"
    agent_file.write_text("print('hello')")

    agent = AgentParser().parse(str(tmp_path))

    dependency_names = [path.split("\\")[-1] for path in agent.dependencies]

    assert "requirements.txt" in dependency_names
    assert "pyproject.toml" in dependency_names


def test_parses_multiple_supported_files(tmp_path):
    (tmp_path / "agent.py").write_text("print('python')")
    (tmp_path / "agent.js").write_text("console.log('javascript')")
    (tmp_path / "config.json").write_text("{}")
    (tmp_path / "config.yaml").write_text("name: test")
    (tmp_path / "config.toml").write_text("name = 'test'")

    agent = AgentParser().parse(str(tmp_path))

    languages = {parsed_file.language for parsed_file in agent.files}

    assert languages == {
        "python",
        "javascript",
        "json",
        "yaml",
        "toml",
    }


def test_ignores_unwanted_directories(tmp_path):
    (tmp_path / "agent.py").write_text("print('main')")

    venv = tmp_path / ".venv"
    venv.mkdir()
    (venv / "fake.py").write_text("print('ignored')")

    git = tmp_path / ".git"
    git.mkdir()
    (git / "fake.py").write_text("print('ignored')")

    node_modules = tmp_path / "node_modules"
    node_modules.mkdir()
    (node_modules / "fake.js").write_text("console.log('ignored')")

    agent = AgentParser().parse(str(tmp_path))

    paths = [parsed_file.path for parsed_file in agent.files]

    assert any(path.endswith("agent.py") for path in paths)
    assert not any(".venv" in path for path in paths)
    assert not any(".git" in path for path in paths)
    assert not any("node_modules" in path for path in paths)


def test_invalid_python_does_not_crash_parser(tmp_path):
    agent_file = tmp_path / "broken.py"
    agent_file.write_text("""
def broken(
    this is invalid python
""")

    agent = AgentParser().parse(str(agent_file))

    assert len(agent.files) == 1
    assert agent.files[0].language == "python"
    assert agent.files[0].functions == []


def test_missing_path_raises_error(tmp_path):
    missing_path = tmp_path / "does_not_exist"

    try:
        AgentParser().parse(str(missing_path))
        assert False, "Expected FileNotFoundError"
    except FileNotFoundError:
        pass
