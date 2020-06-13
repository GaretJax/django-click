import djclick as click


@click.command()
def command():
    click.secho("stdout", fg="blue", nl=False)
    click.secho("stderr", bg="red", err=True, nl=False)
