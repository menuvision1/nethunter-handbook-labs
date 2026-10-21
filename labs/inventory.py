"""Parse a trusted lab Nmap XML file. Origin is declared, never inferred."""
import argparse
import json
import xml.etree.ElementTree as ET

def inventory(path, origin='supplied_fixture'):
    root = ET.parse(path).getroot()
    if root.tag != 'nmaprun':
        raise ValueError('Expected an Nmap XML document')
    rows=[]
    for host in root.findall('host'):
        addresses=host.findall('address')
        addr=next((a.get('addr') for a in addresses if a.get('addrtype') in ('ipv4','ipv6')),None)
        if addr is None:
            raise ValueError('Host lacks IP address')
        for port in host.findall('./ports/port'):
            state=port.find('state')
            if state is None or state.get('state') is None:
                raise ValueError('Port lacks state')
            service=port.find('service')
            rows.append({'addr':addr,'port':int(port.get('portid')),
                         'state':state.get('state'),
                         'service':service.get('name') if service is not None else None,
                         'source':origin})
    return {'assets':rows,'count':len(rows)}

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('file')
    p.add_argument('--origin',choices=['supplied_fixture','owned-scan'],default='supplied_fixture')
    args=p.parse_args()
    print(json.dumps(inventory(args.file,args.origin),indent=2))
