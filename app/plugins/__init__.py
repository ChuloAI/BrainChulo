import importlib
import pkgutil
import os

def load_plugins(app):
    # Get the current directory
    plugins_dir = os.path.dirname(__file__)

    # Iterate over the files in the plugins directory
    for _, plugin_name, is_package in pkgutil.iter_modules([plugins_dir]):
        if is_package:
            # Dynamically import the routes module from each plugin
            plugin_module = importlib.import_module(f"plugins.{plugin_name}.routes")

            # Get the router from the plugin's routes module
            router = plugin_module.router

            # Include the plugin's routes in the main FastAPI app
            app.include_router(router, prefix=f"/plugins/{plugin_name}")

