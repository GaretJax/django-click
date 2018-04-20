import djclick as click


@click.command()
@click.option('-r', '--raise', 'raise_when_called', is_flag=True)
def command(raise_when_called):
    if raise_when_called:
        raise RuntimeError()
