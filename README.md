# GasterBlacklist

Short list of malicious/advertisement sites. 

It includes two lists (`hosts` and `hosts.txt`) which contain the urls in two different formats.

It also includes a small python script to add and remove urls from the list with ease. Just call `main.py` and use 
the command `help` to see all commands and their descriptions.

`hosts` as the name implies can be used as a hosts file for your favorite os. Since it is based on StevensBlacklist, 
it should be functional from get go.

`hosts.txt` uses the same urls and is in fact not much different to the `hosts` file, other than just listing all urls
without prefixing it with "0.0.0.0" as such it can be used for programs such as PortMaster which want it in this format.

This list can be and is being actively used in a Pi-Hole.
