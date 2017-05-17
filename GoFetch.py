"""
GoFetch 1.2
GoFetch displays information about your operating system, like uname on steroids. 
(C) Dylan Hamer 2016
"""

"""Import stuff"""
import click                          # Lovely formatting!
from datetime import timedelta        # For formatting time strings
from platform import system, release  # For getting OS and Version

"""Get uptime and return it in H:M:S format"""
def getUptime():
    with open('/proc/uptime', 'r') as f:
        totalUptime = float(f.readline().split()[0])
    uptime = str(timedelta(seconds = totalUptime)).split(":")
    hours = uptime[0]
    minutes = uptime[1]
    seconds = uptime[2]
    return hours, minutes, seconds

"""Show OS info"""
def showOSInfo():
    click.echo(click.style("OS Information", fg='red'))
    click.echo("")
    click.echo("OS: {p}".format(p=system()))
    click.echo("OS Version: {r}".format(r=release()))
    click.echo("")

def showUptime():
    click.echo(click.style("Uptime", fg='red'))
    click.echo("")
    hours, minutes, seconds = getUptime()
    click.echo("{h} hours".format(h=hours))
    click.echo("{m} minutes".format(m=minutes))
    click.echo("{s} seconds".format(s=seconds))
    click.echo("")

"""Main function"""
@click.command()
@click.option("--osversion", is_flag=True)
@click.option("--os", is_flag=True)
@click.option("--version", is_flag=True)
def main(os, osversion, version):
    if osversion:
        click.echo("OS Version: {r}".format(r=release()))
    elif os:
        click.echo("Platform: {p}".format(p=system()))
    elif version:
        click.echo("GoFetch Version 2.1")
    else:
        showOSInfo()
        showUptime()

if __name__ == "__main__":
    main()
            
                

