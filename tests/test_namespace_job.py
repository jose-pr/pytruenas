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


# -- job-ness of a `_create`/`_update` answer comes from the schema ---------------


class _Schemas:
    """A faked `conn` with `core.get_methods` flags and a `group.create` that
    answers with an int (a record id or a job id)."""

    def __init__(self, flags, answer=5, jobs=None):
        self.wire = []
        self.flags = flags
        self.answer = answer
        self.jobs = jobs or {}
        self._closed = type("Open", (), {"is_set": lambda self: False})()

    def call(self, method, *params, **kwds):
        self.wire.append(method)
        if method == "system.info":
            return {"version": "26.0"}
        if method == "core.get_methods":
            assert params == ("group",)
            return {name: {"job": job} for name, job in self.flags.items()}
        if method == "group.query":
            return []
        if method == "core.get_jobs":
            job_id = params[0][0][2]
            return [self.jobs[job_id]] if job_id in self.jobs else []
        return self.answer


@pytest.fixture
def _cache(tmp_path, monkeypatch):
    monkeypatch.setenv("PYTRUENAS_CACHE", str(tmp_path))


def test_a_record_id_is_not_waited_on(_cache):
    """`group.create` answers with the new id, and job 5 belongs to another."""
    conn = _Schemas(
        {"group.create": False},
        jobs={5: {"id": 5, "state": "SUCCESS", "result": "unrelated", "progress": {}}},
    )
    host = _host(conn)
    assert host.api.group._create(name="svc") == 5
    assert "core.get_jobs" not in conn.wire


def test_a_job_id_is_waited_on(_cache):
    conn = _Schemas(
        {"group.create": True},
        jobs={5: {"id": 5, "state": "SUCCESS", "result": {"id": 9}, "progress": {}}},
    )
    assert _host(conn).api.group._create(name="svc") == {"id": 9}


def test_the_flags_are_read_once_per_service(_cache):
    conn = _Schemas({"group.create": False})
    host = _host(conn)
    host.api.group._create(name="a")
    host.api.group._create(name="b")
    assert conn.wire.count("core.get_methods") == 1


def test_unreadable_flags_wait_on_nothing_and_say_so(_cache, caplog):
    """Asked after the create ran: a refused `core.get_methods` must not turn
    that success into an error."""
    from pytruenas import ClientException

    class Refusing(_Schemas):
        def call(self, method, *params, **kwds):
            if method == "core.get_methods":
                self.wire.append(method)
                raise ClientException("[EPERM] not allowed", errno.EPERM)
            return super().call(method, *params, **kwds)

    conn = Refusing({})
    with caplog.at_level("WARNING", logger="pytruenas"):
        assert _host(conn).api.group._create(name="svc") == 5
    assert "core.get_jobs" not in conn.wire
    assert "job=True" in caplog.text
