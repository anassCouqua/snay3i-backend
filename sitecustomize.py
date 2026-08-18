"""Runtime hardening for Snay3i backend.

FastAPI currently configures Starlette CORS with a wildcard origin while
allowing credentials. Browsers reject that combination for credentialed
cross-origin requests. Normalize it to the production frontend origins
before the app imports CORSMiddleware.
"""

try:
    from starlette.middleware.cors import CORSMiddleware

    _original_init = CORSMiddleware.__init__

    def _patched_init(self, app, *args, **kwargs):
        allow_origins = kwargs.get("allow_origins", args[0] if len(args) > 0 else ())
        allow_credentials = kwargs.get("allow_credentials", args[3] if len(args) > 3 else False)

        if allow_credentials and list(allow_origins) == ["*"]:
            kwargs["allow_origins"] = [
                "https://snay3i.ma",
                "https://www.snay3i.ma",
            ]

        return _original_init(self, app, *args, **kwargs)

    CORSMiddleware.__init__ = _patched_init
except Exception:
    # Never prevent the backend from starting because of this compatibility shim.
    pass
