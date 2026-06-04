"""V-model System 11000 - Lighting.

Headlamps and tail lamps currently live inside the front/rear fascia modules
(``s10000_exterior.frontend`` / ``rearend``); ``lighting.py`` here is not yet
wired into the build.  A later phase extracts the lamp assemblies into this
package.  Returns an empty list for now (no behaviour change).
"""
from __future__ import annotations


def parts():
    return []
