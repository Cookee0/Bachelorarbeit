# Write the ontology reference file for the manual review of the generated context.
# It's extracted directly from the official ontology file (insurance.ttl).

import rdflib
from rdflib.namespace import OWL, RDF, RDFS

from db import BENCH, ROOT

graph = rdflib.Graph().parse(BENCH / "ontology/insurance.ttl")
PREFIX = "http://data.world/schema/insurance/"


def short(uri):
    """Strip the ontology prefix / XSD namespace; empty -> '(untyped)'."""
    if not uri:
        return "(untyped)"
    return (
        str(uri).removeprefix(PREFIX).removeprefix("http://www.w3.org/2001/XMLSchema#")
    )


def terms(rdf_type):
    for s in sorted(set(graph.subjects(RDF.type, rdf_type))):
        yield (
            short(s),
            graph.value(s, RDFS.label),
            graph.value(s, RDFS.domain),
            graph.value(s, RDFS.range),
        )


lines = [
    f"# Prefix: {PREFIX}",
    "# domain = class the property belongs to (subject)",
    "# range  = target class (relationship) or datatype (attribute)",
    "",
    "CLASSES (name | label)",
]
lines += [f"{n} | {l}" for n, l, _, _ in terms(OWL.Class)]

lines += ["", "RELATIONSHIPS (name | label | domain -> range)"]
lines += [
    f"{n} | {l} | {short(d)} -> {short(r)}" for n, l, d, r in terms(OWL.ObjectProperty)
]

lines += ["", "ATTRIBUTES (name | label | domain : datatype)"]
lines += [
    f"{n} | {l} | {short(d)} : {short(r)}" for n, l, d, r in terms(OWL.DatatypeProperty)
]

with open(ROOT / "context/ontology_reference.txt", "w", encoding="utf-8") as file:
    file.write("\n".join(lines) + "\n")
