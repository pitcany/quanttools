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

# Locking and installing specific groups

To generate or install dependencies for a single optional group (e.g. `optimization`) without pulling in conflicting packages like TensorFlow, Poetry 2.4+ supports the `--only` flag:

```bash
poetry lock --only optimization
poetry install --only optimization
```

If you are on Poetry 2.2.x and cannot yet upgrade, consider using the `poetry_only_data_ml.txt` guide for workarounds or upgrading Poetry:

```bash
pipx upgrade poetry
```

# Optional Autogluon support

This project provides an optional `autogluon` dependency group to avoid dependency conflicts.
You can enable this group when locking or installing dependencies:

```bash
poetry lock --with autogluon
poetry install --with autogluon
```

For Poetry 2.4+ you can also restrict to only the `autogluon` group:

```bash
poetry lock --only autogluon
poetry install --only autogluon
```

To add Autogluon to your project, run:

```bash
poetry add autogluon-core --group autogluon
# or for full tabular support:
poetry add 'autogluon.tabular[all]' --group autogluon
```
