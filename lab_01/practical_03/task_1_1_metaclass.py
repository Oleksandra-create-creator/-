from abc import ABC, abstractmethod
import hashlib


class PluginMeta(type):
    _registry: dict[str, type] = {}
    REQUIRED_ATTRS = ("name", "version")

    def __new__(mcs, cls_name: str, bases: tuple, namespace: dict):
        cls = super().__new__(mcs, cls_name, bases, namespace)
        if bases and bases != (ABC,):
            for attr in mcs.REQUIRED_ATTRS:
                if attr not in namespace:
                    raise TypeError(f"Плагін {cls_name} повинен мати атрибут '{attr}'")
            if "name" in namespace:
                mcs._registry[namespace["name"]] = cls
        return cls

    @classmethod
    def get_registry(mcs) -> dict[str, type]:
        return mcs._registry.copy()

    @classmethod
    def create_plugin(mcs, plugin_name: str):
        if plugin_name not in mcs._registry:
            raise ValueError(f"Плагін '{plugin_name}' не знайдено")
        return mcs._registry[plugin_name]()


class BasePlugin(ABC, metaclass=PluginMeta):
    @abstractmethod
    def execute(self, data: str) -> str:
        pass


class UpperPlugin(BasePlugin):
    name = "upper"
    version = "1.0"

    def execute(self, data: str) -> str:
        return data.upper()


class ReversePlugin(BasePlugin):
    name = "reverse"
    version = "1.0"

    def execute(self, data: str) -> str:
        return data[::-1]


class CensorPlugin(BasePlugin):
    name = "censor"
    version = "1.1"
    _banned = ["Світ", "погано"]

    def execute(self, data: str) -> str:
        result = data
        for word in self._banned:
            result = result.replace(word, "***")
        return result


HashPlugin = type(
    "HashPlugin",
    (BasePlugin,),
    {
        "name": "hash",
        "version": "2.0",
        "execute": lambda self, data: hashlib.sha256(data.encode()).hexdigest(),
    },
)


def main():
    print("Зареєстровані плагіни:")
    for name, cls in PluginMeta.get_registry().items():
        print(f"  {name} (v{cls.version}): {cls.__name__}")

    test_data = "Привіт Світ"
    print(f"\nТестові дані: '{test_data}'")
    for name in PluginMeta.get_registry():
        plugin = PluginMeta.create_plugin(name)
        print(f"  {name}: {plugin.execute(test_data)}")

    print("\nПеревірка валідації метакласу:")
    try:
        class BadPlugin(BasePlugin):
            version = "1.0"
    except TypeError as e:
        print(f"  Перехоплено: {e}")


if __name__ == "__main__":
    main()
