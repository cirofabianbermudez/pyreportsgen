from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("pyrepgen")
except PackageNotFoundError:
    __version__ = "0.0.0"

# from .gen_report import generate_report

# __all__ = [
#     "__version__",
#     "generate_report",
# ]
