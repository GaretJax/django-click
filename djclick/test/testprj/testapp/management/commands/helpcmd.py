import djclick as click


@click.command()
def command():
    # Just print some things which shall not be found in the output
    click.echo('HELP_CALLED')
