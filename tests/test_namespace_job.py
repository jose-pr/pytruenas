"""`job=True` on a middleware call waits for the job, as the upstream client
does, instead of returning the job id while the job still runs."""

import errno

import pytest

from pytruenas import TrueNASClient
from pytruenas.connection import JobFailed


class _Middleware:
    """A faked `conn` whose job-starting method answers with job 42."""

    def __init__(self, state="SUCCESS", start_result=42):
        self.wire = []
        self.state = state
        self.start_result = start_result
        self._closed = type("Open", (), {"is_set": lambda self: False})()

    def call(self, method, *params, **kwds):
        self.wire.append((method, params, kwds))
        if method == "core.get_jobs":
            return [
                {
                    "id": 42,
                    "state": self.state,
                    "result": "deleted" if self.state == "SUCCESS" else None,
                    "error": "[EBUSY] dataset is busy",
                    "exc_info": {"errno": errno.EBUSY},
                    "progress": {"percent": 100},
                }
            ]
        return self.start_result


def _host(middleware):
    host = TrueNASClient("wss://nas.example", autologin=False)
    host._conn = middleware
    return host


def test_job_true_returns_the_jobs_result():
    middleware = _Middleware()
    assert _host(middleware).api.pool.dataset.delete("tank/x", job=True) == "deleted"
    assert middleware.wire[0] == ("pool.dataset.delete", ("tank/x",), {})
    assert [m for m, _, _ in middleware.wire[1:]] == ["core.get_jobs"]


def test_job_true_raises_a_failed_job():
    host = _host(_Middleware(state="FAILED"))
    with pytest.raises(JobFailed, match="dataset is busy"):
        host.api.pool.dataset.delete("tank/x", job=True)


def test_job_true_maps_a_failed_job_to_oserror_on_request():
    host = _host(_Middleware(state="FAILED"))
    with pytest.raises(OSError) as error:
        host.api.pool.dataset.delete("tank/x", job=True, _ioerror=True)
    assert error.value.errno == errno.EBUSY


def test_without_job_the_id_comes_back_at_once():
    middleware = _Middleware()
    assert _host(middleware).api.pool.dataset.delete("tank/x") == 42
    assert [m for m, _, _ in middleware.wire] == ["pool.dataset.delete"]


@pytest.mark.parametrize("answer", [True, None, {"id": 1}])
def test_job_true_on_a_method_that_is_not_a_job_returns_its_answer(answer):
    middleware = _Middleware(start_result=answer)
    assert _host(middleware).api.core.ping(job=True) == answer
    assert len(middleware.wire) == 1


def test_job_return_keeps_the_job_id():
    middleware = _Middleware()
    assert _host(middleware).api.pool.dataset.delete("x", job="RETURN") == 42
    assert len(middleware.wire) == 1
