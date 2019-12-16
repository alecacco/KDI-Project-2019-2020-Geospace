import os

linked_data_dir = './data/linked_data'

files = [os.path.join(dp, f) for dp, dn, fn in os.walk(os.path.expanduser(linked_data_dir)) for f in fn]
files = sorted(filter(lambda x: x.endswith('RDF.ttl'), files))

final_ttl = open(f'{linked_data_dir}/GeoSpace_RDF.ttl', 'w+')
for ttl in files:
    f = open(ttl, 'r')
    final_ttl.write(f.read())
    f.close()

final_ttl.close()