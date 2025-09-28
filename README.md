# Removing installed packages

To remove a dependency from your project (and uninstall it from your venv), use:

```bash
poetry remove <package-name>
```

If the package is in a specific group, specify the group via:

```bash
poetry remove <package-name> --group <group-name>
# or equivalently for dev dependencies:
poetry remove <package-name> --dev
```
