"""
GoFetch 1.2
GoFetch displays information about your operating system, like uname on steroids. 
(C) Dylan Hamer 2016
"""

"""Import stuff"""
import click                          # Lovely formatting!
from datetime import timedelta        # For formatting time strings
from platform import system, release  # For getting OS and Version

"""Decorator to handle exceptions"""
def handleExceptions(function):
    def handle():
        try:
            function()
        except NotImplementedError as exception:
            exceptionName = "NotImplementedException."
            exceptionExplanation = "This option hasn't been implemented yet."
            exceptionErrorCode = 1
            exceptionType = "Warning"
            exceptionSuggestedActions = "Please give the developer a poke."
        except BaseException as exception:
            exceptionName = "BaseException"
            exceptionExplanation = exception
            exceptionErrorCode = 2
            exceptionType = "Fatal"
            exceptionSuggestedActions = "Please visit https://github.com/DylanHamer/GoFetch/issues to report an issue."
        click.secho("\nSomething went wrong!", fg='red')
        click.secho("""Error: {en}\nExplanation: {ee}\nSuggested Actions: {sa}\n""".format(
                                                                                           en=exceptionName,
                                                                                           ee=exceptionExplanation,
                                                                                           sa=exceptionSuggestedActions
                                                                                           ), 
                                                                                           fg='yellow'
                                                                                           )
        if exceptionType == "Fatal":
            exit(exceptionErrorCode)
    return handle

"""Decorator to format text"""
def format(function):
    @handleExceptions
    @click.command()
    @click.option('--highlightcolor', default='blue')
    @click.option('--textcolor', default='white')
    def formatText(highlightcolor, textcolor):
        showText = function().showText
        for textItem in showText:
            newline = True
            color = textcolor
            if "/h" in textItem:
                color = highlightcolor
            elif "/o" in textItem:
                newline = False
            click.secho(textItem, fg=color, nl=newline) 
    return formatText

"""Get uptime and return it in H:M:S format"""
def getUptime():
    with open('/proc/uptime', 'r') as f:
        totalUptime = float(f.readline().split()[0])
    uptime = str(timedelta(seconds = totalUptime)).split(":")
    hours = uptime[0]
    minutes = uptime[1]
    seconds = uptime[2]
    return hours, minutes, seconds

"""Get OS info"""
def getOSInfo():
    osName = system()
    osVersion = release()
    return osName, osVersion

"""Show info"""
@format
def showOSInfo():            
    osName, osVersion = getOSInfo()
    uptimeHours, uptimeMinutes, uptimeSeconds = getUptime()
    showText = [
                "/hOS:/o",
                osName,
                "/hOS Version:/o",
                osVersion,
                "/hUptime/o:",
                uptimeHours+" hours /o",
                uptimeMinutes+" minutes /o",
                uptimeSeconds+" seconds /o"
               ]

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
            
                

