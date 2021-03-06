from kong_config_builder import *  # noqa


key_auth_plugin = Plugin(
    name="key-auth",
    enabled=True)

Kong(
    services=[
        Service(
            name="test_name",
            host="test_upstream",
            routes=[
                Route(
                    name="test_route",
                    paths=[
                        "/"
                    ],
                    strip_path=False
                )
            ]
        ),
        Service(
            name="auth_name",
            host="test_upstream",
            routes=[
                Route(
                    name="auth_route",
                    paths=[
                        "/auth"
                    ],
                    strip_path=True
                )
            ],
            plugins=[
                key_auth_plugin
            ]
        )
    ],
    upstreams=[
        Upstream(
            name="test_upstream",
            targets=[Target(
                "www.google.com:80"
            )],
            healthchecks=Healthcheck(
                active=HealthcheckActive(
                    type="http",
                    http_path="/",
                    timeout=100.0,
                    concurrency=1,
                    healthy=HealthcheckHealthy(
                        interval=1,
                        successes=1,
                        http_statuses=[200]
                    ),
                    unhealthy=HealthcheckUnhealthy(
                        interval=1,
                        timeouts=2,
                        http_failures=1
                    )
                )
            )
        )
    ],
    plugins=[
        Plugin(name="prometheus", enabled=False)
    ],
    consumers=[
        Consumer(username="test_consumer")
    ],
    keyauth_credentials=[
        KeyauthCredential(consumer="test_consumer", key="pass1234")
    ]
).save()
