import os

from spec import Spec

from invoke import run

from _util import assert_cpu_usage


class Runner_(Spec):
    class responding:
        # TODO: update respond_*.py so they timeout instead of hanging forever
        # when not being responded to

        def setup(self):
            os.chdir(os.path.join(os.path.dirname(__file__), '_support'))

        def base_case(self):
            # Basic "doesn't explode" test: respond.py will exit nonzero unless
            # this works, causing a Failure.
            responses = {r"What's the password\?": "Rosebud\n"}
            # Gotta give -u or Python will line-buffer its stdout, so we'll
            # never actually see the prompt.
            run("python -u respond_base.py", responses=responses, hide=True)

        def both_streams(self):
            responses = {
                "standard out": "with it\n",
                "standard error": "between chair and keyboard\n",
            }
            run("python -u respond_both.py", responses=responses, hide=True)

        def stdin_mirroring_isnt_cpu_heavy(self):
            "stdin mirroring isn't CPU-heavy"
            with assert_cpu_usage(lt=5.0):
                run("python -u busywork.py 10", pty=True, hide=True)
