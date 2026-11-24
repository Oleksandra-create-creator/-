class ValidatedField:
    def __init__(self, expected_type: type, min_value=None, max_value=None):
        self.expected_type = expected_type
        self.min_value = min_value
        self.max_value = max_value

    def __set_name__(self, owner, name):
        self.public_name = name
        self.private_name = f"_{name}"

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.private_name)

    def __set__(self, obj, value):
        if not isinstance(value, self.expected_type):
            raise TypeError(f"Поле '{self.public_name}' має бути типу {self.expected_type.__name__}")
        if self.min_value is not None and value < self.min_value:
            raise ValueError(f"Значення '{self.public_name}' має бути >= {self.min_value}")
        if self.max_value is not None and value > self.max_value:
            raise ValueError(f"Значення '{self.public_name}' має бути <= {self.max_value}")
        setattr(obj, self.private_name, value)


class ConfigSection:
    _sections: dict[str, type] = {}

    def __init_subclass__(cls, section_name: str = "", **kwargs):
        super().__init_subclass__(**kwargs)
        if section_name:
            cls._sections[section_name] = cls

    @classmethod
    def get_section(cls, name: str):
        return cls._sections.get(name)

    @classmethod
    def list_sections(cls) -> list[str]:
        return list(cls._sections.keys())


class DatabaseConfig(ConfigSection, section_name="database"):
    host = ValidatedField(str)
    port = ValidatedField(int, min_value=1, max_value=65535)
    max_connections = ValidatedField(int, min_value=1, max_value=1000)

    def __init__(self, host: str, port: int, max_connections: int):
        self.host = host
        self.port = port
        self.max_connections = max_connections


class LoggingConfig(ConfigSection, section_name="logging"):
    level = ValidatedField(str)
    max_file_size_mb = ValidatedField(int, min_value=1, max_value=1024)

    def __init__(self, level: str, max_file_size_mb: int):
        self.level = level
        self.max_file_size_mb = max_file_size_mb


def main():
    print("Зареєстровані секції:", ConfigSection.list_sections())

    print("\nСтворення коректної конфігурації:")
    db = DatabaseConfig(host="localhost", port=5432, max_connections=100)
    print(f"  DB: {db.host}:{db.port} (max_conn: {db.max_connections})")

    print("\nПеревірка валідації типу:")
    try:
        db.port = "not_a_number"
    except TypeError as e:
        print(f"  Перехоплено: {e}")

    print("\nПеревірка валідації діапазону:")
    try:
        db.port = 70000
    except ValueError as e:
        print(f"  Перехоплено: {e}")


if __name__ == "__main__":
    main()
