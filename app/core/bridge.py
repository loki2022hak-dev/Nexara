import scanner
import boost

class ModuleRegistry:
    def __init__(self):
        self.modules = {
            "NetworkScanner": scanner.scan_network,
            "SystemBoost": boost.boost_volume
        }
module_registry = ModuleRegistry()
