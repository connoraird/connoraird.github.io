"""Nox config."""

import os
import pathlib
import shutil

import nox
import nox_uv

# Options to modify nox behaviour
nox.options.default_venv_backend = "uv"
nox.options.reuse_existing_virtualenvs = True

ARRAY_BACKENDS = {
    "array_api_strict": "array-api-strict>=2",
    "jax": "jax>=0.4.32",
}
BENCH_TESTS_LOC = pathlib.Path("tests/benchmarks")


@nox_uv.session(
    uv_no_install_project=True,
    uv_only_groups=["test"],
)
def regression_tests(session: nox.Session) -> None:
    """
    Run regression benchmark tests between two revisions.

    Note it is not possible to pass extra options to pytest.

    """
    # Check for valid user input
    expected_count = 2
    if not session.posargs:
        msg = f"{expected_count} revision(s) not provided"
        raise ValueError(msg)

    if len(session.posargs) != expected_count:
        msg = (
            f"Incorrect number of revisions provided ({len(session.posargs)}), "
            f"expected {expected_count}"
        )
        raise ValueError(msg)

    before_revision, after_revision = session.posargs

    # Install the correct array-backends based on environment variables
    array_backend = os.environ.get("ARRAY_BACKEND")
    if array_backend == "array_api_strict":
        session.install(ARRAY_BACKENDS["array_api_strict"])
    elif array_backend == "jax":
        session.install(ARRAY_BACKENDS["jax"])
    elif array_backend == "all":
        session.install(*ARRAY_BACKENDS.values())

    # make sure benchmark directory is clean
    benchmark_dir = pathlib.Path(".benchmarks")
    if benchmark_dir.exists():
        session.log(f"Deleting previous benchmark directory: {benchmark_dir}")
        shutil.rmtree(benchmark_dir)

    # Generate starting state benchmark
    session.log(f"Generating prior benchmark from revision {before_revision}")
    session.install(f"git+https://github.com/glass-dev/glass@{before_revision}")
    session.run(
        "pytest",
        BENCH_TESTS_LOC,
        "--benchmark-autosave",
        "--benchmark-calibration-precision=1000",
        "--benchmark-columns=mean,stddev,rounds",
        "--benchmark-max-time=5.0",
        "--benchmark-sort=name",
        "--benchmark-timer=time.process_time",
    )

    # Generate and compare "stable" benchmark tests
    session.log(f"Comparing {before_revision} benchmark to revision {after_revision}")
    session.install(f"git+https://github.com/glass-dev/glass@{after_revision}")
    session.log("Running stable regression tests")
    session.run(
        "pytest",
        BENCH_TESTS_LOC,
        "-m",
        "stable",
        "--benchmark-compare=0001",
        "--benchmark-compare-fail=mean:5%",
        "--benchmark-calibration-precision=1000",
        "--benchmark-columns=mean,stddev,rounds",
        "--benchmark-max-time=5.0",
        "--benchmark-sort=name",
        "--benchmark-timer=time.process_time",
    )

    # Generate and compare "unstable" benchmark tests
    session.log("Running unstable regression tests")
    session.run(
        "pytest",
        BENCH_TESTS_LOC,
        "-m",
        "unstable",
        "--benchmark-compare=0001",
        # Absolute time comparison in seconds
        "--benchmark-compare-fail=mean:0.0005",
        "--benchmark-calibration-precision=1000",
        "--benchmark-columns=mean,stddev,rounds",
        "--benchmark-max-time=5.0",
        "--benchmark-sort=name",
        "--benchmark-timer=time.process_time",
    )
