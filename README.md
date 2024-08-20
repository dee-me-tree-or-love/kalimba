# 🐳 `Kalimba` == `Co'li`ma `M`enu `Ba`r

> 🌱 This is an early WIP, more information coming soon ✨

`kalimba` is a tiny menu bar application allowing to monitor and toggle
the status of [`colima`](https://github.com/abiosoft/colima) with a basic GUI
written using [`rumps`](https://github.com/jaredks/rumps).

## Usage

### Start the `kalimba` menu bar app

```bash
$ kalimba
INFO:kalimba.kalimba:Starting the kalimba app... 🎶
...
```

> 🧙 and it launches the `kalimba` 🐳 application! ✨
>
> ![kalimba-menu-bar](docs/assets/kalimba-basic.png)

### Getting `kalimba` help

```bash
$ kalimba --help
Usage: kalimba [OPTIONS] ...
```

## Installation

### Give it a local try

Starting right away using [`poetry`](https://python-poetry.org/):

```bash
poetry install # installs kalimba in poetry's environment
poetry run kalimba --help # shows some tips-and-tricks
poetry run kalimba # starts the app
```
<!-- markdownlint-disable MD033 -->
<details open="true">
<summary><i>More temporary installation options</i> 👀</summary>

<details>
<summary><b>Using local build</b> 🪵</summary>

#### Install local build directly

1. Build the project

    ```bash
    $ poetry build
    Building kalimba (<version>)
     ...
     - Built kalimba-<version>-.tar.gz
     ...
    ```

2. Check build results:

    ```bash
    $ ls ./dist
    ...
    kalimba-<version>-.tar.gz
    ...
    ```

3. Install the local `tar` file:

    > Don't forget to replace the `<version>` to the built result. 💡

    ```bash
    $ pip install --user ./dist/kalimba-<version>-.tar.gz
    ...
    Successfully installed ... kalimba-<version> ...
    ```

4. Check direct access to `kalimba` CLI

    ```bash
    $ kalimba --help

    Usage: kalimba [OPTIONS]
    ...
    ```

</details>

<details>
<summary><b>Using pypiserver</b> 🏕️</summary>

#### Install via (local) [pypiserver](https://github.com/pypiserver/pypiserver)

1. Start the local [`pypi-server`](https://github.com/pypiserver/pypiserver)

    > This guide shows how to use a locally running pypiserver.  
    > Feel free to skip to the next step if you already have one running elsewhere. ✌️

    ```bash
    docker run --rm -p 80:8080 pypiserver/pypiserver:latest run -P . -a . -vvv
    ```

2. Configure `poetry`:

    > If you would like to use a remotely deployed one, feel free to
    > adjust the pypiserver URLs here and further. 🔁

    ```bash
    poetry config repositories.local http://localhost 
    ```

3. Build and publish the project

    ```bash
    $ poetry build
    Building kalimba (<version>)
     ...
     - Built kalimba-<version>-...
    $ poetry publish -r local
    Publishing kalimba (<version>) to local
    ...
    $ pip install --user -i http://localhost/ kalimba
    ...
    Successfully installed ... kalimba-<version> ...
    ```

4. Check direct access to `kalimba` CLI

    ```bash
    $ kalimba --help

    Usage: kalimba [OPTIONS]
    ...
    ```

</details>
</details>
<!-- markdownlint-enable MD033 -->
