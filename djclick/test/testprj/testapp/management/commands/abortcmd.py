import djclick as click


@click.command()
def command():
    raise click.Abort()
