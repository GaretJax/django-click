import djclick as click


@click.command()
@click.pass_context
def command(ctx):
    assert isinstance(ctx.verbosity, int)
    click.echo(ctx.verbosity, nl=False)
