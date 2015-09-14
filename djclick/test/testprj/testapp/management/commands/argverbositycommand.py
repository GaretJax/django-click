import djclick as click


@click.command()
@click.pass_verbosity
def command(verbosity):
    assert isinstance(verbosity, int)
    click.echo(verbosity, nl=False)
