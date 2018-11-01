class TestConfig:
    TESTING = True

class DevelopmentConfig:
    TESTING = False

config_env = {
    "testing": TestConfig,
    "development": DevelopmentConfig
}
