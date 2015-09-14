import djclick as click


@click.group(invoke_without_command=True)
def main():
    click.echo('group_command')


@main.command()
def subcmd1():
    click.echo('SUB1')


@main.command(name='subcmd3')
def subcmd2():
    click.echo('SUB2')
