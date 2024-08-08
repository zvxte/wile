# Wile

**Solve chess puzzles from your own games**.

## Setup

Create virtual environment, then install dependencies.
On Linux:
```bash
cd wile
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
See [example](./src/example.py).

## Todo

- Chess library implementation in C
- Database support (Sqlite implementation for local use)
- Server API using [Starlette](https://github.com/encode/starlette) framework
- Simple frontend for graphical use

## Disclaimer

This is a personal project created for learning purposes and is **not suitable** for real-world usage.

## License

This project is licensed under [GPL-3.0 license](./LICENSE).
