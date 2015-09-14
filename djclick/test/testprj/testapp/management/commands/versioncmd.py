import djclick as click


@click.command(version='20.0')
def command():
    raise RuntimeError()  # NOCOV
