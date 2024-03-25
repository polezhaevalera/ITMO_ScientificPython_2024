# -*- coding: utf-8 -*-
"""HW2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1u9UnXD33yIjtxNF30zDjdKrx046Eb3vC
"""

import requests
import json
import re
import numpy as np

def get_uniprot(ids: list):
  accessions = ','.join(ids)
  endpoint = "https://rest.uniprot.org/uniprotkb/accessions"
  http_function = requests.get
  http_args = {'params': {'accessions': accessions}}
  return http_function(endpoint, **http_args)

def uniprot_parse_response(resp: dict):
    resp = resp.json()
    resp = resp["results"]
    output = {}
    for val in resp:
        acc = val['primaryAccession']
        species = val['organism']['scientificName']
        gene = val['genes']
        seq = val['sequence']
        output[acc] = {'organism':species, 'geneInfo':gene, 'sequenceInfo':seq, 'type':'protein'}

    return output

def get_ensembl(ids: list):
  id = json.dumps({'ids': ids})
  endpoint = "https://rest.ensembl.org/lookup/id"
  headers={ "Content-Type" : "application/json", "Accept" : "application/json"}
  http_function = requests.post
  http_args = {'headers': headers,'data': id}
  return http_function(endpoint, **http_args)

def ensembl_parse_response(resp: dict):
    resp = resp.json()
    output = {}
    for key,value in resp.items():
        species = value['species']
        canonical_transcript = value['canonical_transcript']
        descr = value['description']
        otype = value['object_type']
        biotype = value['biotype']
        start = value['start']
        end = value['end']
        output[key] = {'organism':species, 'canonical_transcript': canonical_transcript, 'start': start, 'end': end, 'Info':descr, 'object_type':otype, 'biotype':biotype}
    return output

def uniprot_or_ensembl_parse(ids: list):
  if np.all([bool(re.match('ENS[A-Z]{1,4}[0-9]{11}|MGP_[A-Za-z0-9]{2,10}_(E|G|P|R|T|GT|FM)[0-9]+', gene)) for gene in ids]):
    print("Ens")
    resp = get_ensembl(ids)
    output = ensembl_parse_response(resp)
  elif np.all([bool(re.match('[OPQ][0-9][A-Z0-9]{3}[0-9]|[A-NR-Z][0-9]([A-Z][A-Z0-9]{2}[0-9]){1,2}', gene)) for gene in ids]):
    print("Uni")
    resp = get_uniprot(ids)
    output = uniprot_parse_response(resp)
  else:
    raise TypeError('No matches')
  return output

