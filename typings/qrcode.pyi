import io

class QRCode:
    def add_data(self, data: str) -> None: ...

    def print_ascii(*, out: io.StringIO) -> None: ...
