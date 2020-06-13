import djclick as click


@click.command()
@click.argument("arg")
def command(arg):
    click.echo(arg)
