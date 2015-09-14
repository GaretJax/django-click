import djclick as click

import testapp2


@click.command()
def command():
    click.echo(testapp2.FLAG, nl=False)
