#!/usr/bin/env python

"""xml2json.py  Convert XML to JSON

Relies on ElementTree for the XML parsing.  This is based on
pesterfish.py but uses a different XML->JSON mapping.
The XML->JSON mapping is described at
http://www.xml.com/pub/a/2006/05/31/converting-between-xml-and-json.html

Rewritten to a command line utility by Hay Kranen < github.com/hay >

XML                              JSON
<e/>                             "e": null
<e>text</e>                      "e": "text"
<e name="value" />               "e": { "@name": "value" }
<e name="value">text</e>         "e": { "@name": "value", "#text": "text" }
<e> <a>text</a ><b>text</b> </e> "e": { "a": "text", "b": "text" }
<e> <a>text</a> <a>text</a> </e> "e": { "a": ["text", "text"] }
<e> text <a>text</a> </e>        "e": { "#text": "text", "a": "text" }

This is very similar to the mapping used for Yahoo Web Services
(http://developer.yahoo.com/common/json.html#xml).

This is a mess in that it is so unpredictable -- it requires lots of testing
(e.g. to see if values are lists or strings or dictionaries).  For use
in Python this could be vastly cleaner.  Think about whether the internal
form can be more self-consistent while maintaining good external characteristics
for the JSON.

Look at the Yahoo version closely to see how it works.  Maybe can adopt
that completely if it makes more sense...

R. White, 2006 November 6
"""

import xml.etree.cElementTree as ET
import simplejson, optparse, sys, os

def elem_to_internal(elem,strip=1):

    """Convert an Element into an internal dictionary (not JSON!)."""

    d = {}
    for key, value in elem.attrib.items():
        d['@'+key] = value

    # loop over subelements to merge them
    for subelem in elem:
        v = elem_to_internal(subelem,strip=strip)
        tag = subelem.tag
        value = v[tag]
        try:
            # add to existing list for this tag
            d[tag].append(value)
        except AttributeError:
            # turn existing entry into a list
            d[tag] = [d[tag], value]
        except KeyError:
            # add a new non-list entry
            d[tag] = value
    text = elem.text
    tail = elem.tail
    if strip:
        # ignore leading and trailing whitespace
        if text: text = text.strip()
        if tail: tail = tail.strip()

    if tail:
        d['#tail'] = tail

    if d:
        # use #text element if other attributes exist
        if text: d["#text"] = text
    else:
        # text is the value if no attributes
        d = text or None
    return {elem.tag: d}


def internal_to_elem(pfsh, factory=ET.Element):

    """Convert an internal dictionary (not JSON!) into an Element.

    Whatever Element implementation we could import will be
    used by default; if you want to use something else, pass the
    Element class as the factory parameter.
    """

    attribs = {}
    text = None
    tail = None
    sublist = []
    tag = pfsh.keys()
    if len(tag) != 1:
        raise ValueError("Illegal structure with multiple tags: %s" % tag)
    tag = tag[0]
    value = pfsh[tag]
    if isinstance(value,dict):
        for k, v in value.items():
            if k[:1] == "@":
                attribs[k[1:]] = v
            elif k == "#text":
                text = v
            elif k == "#tail":
                tail = v
            elif isinstance(v, list):
                for v2 in v:
                    sublist.append(internal_to_elem({k:v2},factory=factory))
            else:
                sublist.append(internal_to_elem({k:v},factory=factory))
    else:
        text = value
    e = factory(tag, attribs)
    for sub in sublist:
        e.append(sub)
    e.text = text
    e.tail = tail
    return e


def elem2json(elem, strip=1):

    """Convert an ElementTree or Element into a JSON string."""

    if hasattr(elem, 'getroot'):
        elem = elem.getroot()
    return simplejson.dumps(elem_to_internal(elem,strip=strip))


def json2elem(json, factory=ET.Element):

    """Convert a JSON string into an Element.

    Whatever Element implementation we could import will be used by
    default; if you want to use something else, pass the Element class
    as the factory parameter.
    """

    return internal_to_elem(simplejson.loads(json), factory)


def xml2json(xmlstring,strip=1):

    """Convert an XML string into a JSON string."""

    elem = ET.fromstring(xmlstring)
    return elem2json(elem,strip=strip)


def json2xml(json, factory=ET.Element):

    """Convert a JSON string into an XML string.

    Whatever Element implementation we could import will be used by
    default; if you want to use something else, pass the Element class
    as the factory parameter.
    """

    elem = internal_to_elem(simplejson.loads(json), factory)
    return ET.tostring(elem)

def main():
    p = optparse.OptionParser(
        description = 'Converts XML to JSON or the other way around',
        prog = 'xml2json',
        usage = '%prog -t xml2json -o file.json file.xml'
    )
    p.add_option('--type', '-t', help="'xml2json' or 'json2xml'")
    p.add_option('--out', '-o', help="Write to OUT instead of stdout")
    options, arguments = p.parse_args()

    if len(arguments) == 1 :
        input = open(arguments[0]).read()
    else:
        p.print_help()
        sys.exit(-1)

    if (options.type == "xml2json") :
        out = xml2json(input, strip = 0)
    else:
        out = json2xml(input)

    if (options.out) :
        file = open(options.out, 'w')
        file.write(out)
        file.close()
    else:
        print out

if __name__ == "__main__":
    main()