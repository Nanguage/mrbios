from pathlib import Path
import json


DEFAULT_SETTING_PATH = Path.home() / ".mrbios" / "setting.json"


class UserSetting():
    """User setting for mrbios."""
    def __init__(self, path: Path = DEFAULT_SETTING_PATH):
        self.path = path
        if not self.path.exists():
            self.path.parent.mkdir(parents=True, exist_ok=True)
            self.attrs = {}

    @property
    def attrs(self) -> dict:
        """Return the attributes of the user setting."""
        with open(self.path) as f:
            attrs = json.load(f)
        return attrs

    @attrs.setter
    def attrs(self, value: dict):
        """Set the attributes of the user setting."""
        with open(self.path, 'w') as f:
            json.dump(value, f, indent=4)

    def update(self, value: dict):
        """Update the attributes of the user setting."""
        attrs = self.attrs
        attrs.update(value)
        self.attrs = attrs
