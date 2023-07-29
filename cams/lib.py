# CAMS Asset Management System - CTCL 2017-2023
# File: lib.py
# Purpose: Commonly used functions
# Created: May 4, 2023
# Modified: July 27, 2023

from datetime import datetime, timezone
import json, base64
import os
from . import __version__

if os.path.exists("config/config.json"):
    with open("config/config.json") as f:
        jsondata = json.loads(f.read())["config"]
else:
    printe("lib.py ERROR: config/config.json does not exist")

# printe statement that does not raise an exception if the code is running headless
def printe(text):
    try:
        print(text)
    except OSError:
        pass

# Get a specific part/key of the config
def getconfig(part):
    try:
        return jsondata[part]
    except KeyError:
        printe(f"lib.py WARNING: Key \"{part}\" does not exist in config/config.json")
        return None

# Timestamp to formatted date
def dt2fmt(dt):
    # TODO: have strfstr read from a config file
    strfstr = getconfig("misc")["strftime"]

    return dt.strftime(strfstr)

# "Human size" data size formatting
def hsize(fsize):
    suffix = "Bytes"
    
    for unit in [" ", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(fsize) < 1024.0:
            return f"{fsize:3.0f}{unit}{suffix}"
        fsize /= 1024.0
        
    return f"{num:.1f}Yi{suffix}"

# Function to prefill context data to make views smaller
def mkcontext(request, title, scripts = "none"):
    context = {"title": title, "styling": theme(request.COOKIES.get("theme")), "misc": getconfig("misc"), "navbar": getconfig("navbar"), "ver": __version__}
    
    # font - Load just fontawesome
    # form - Load JQuery and Select2
    # table - Load JQuery, fontawesome and tablesorter
    if scripts == "font":
        context["fa"] = True
        context["jq"] = False
        context["ts"] = False
        context["s2"] = False
    elif scripts == "form":
        context["fa"] = False
        context["jq"] = True
        context["ts"] = False
        context["s2"] = True
    elif scripts == "table":
        context["fa"] = True
        context["jq"] = True
        context["ts"] = True
        context["s2"] = False
    else:
        context["fa"] = False
        context["jq"] = False
        context["ts"] = False
        context["s2"] = False
    
    return context

if os.path.exists("themecfg.json"):
    with open("themecfg.json") as f:
        themes = json.loads(f.read())
else:
    printe("lib.py ERROR: themecfg.json does not exist, it may not have been generated yet")
    themes = {}

# Return theme data
def theme(tname):    
    try:
        return themes[tname]
    except KeyError:
        printe(f"lib.py WARNING: Theme \"{tname}\" not found, using default")
        return themes["default"]
        