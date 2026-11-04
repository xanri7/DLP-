def test_server_app_factory():
    from server.app import create_app
    app = create_app()
    assert app is not None
