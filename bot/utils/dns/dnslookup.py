import dns.resolver
import dns.rdatatype
import dns.exception
from collections import defaultdict

RECORDS = [
    dns.rdatatype.A,
    dns.rdatatype.AAAA,
    dns.rdatatype.MX,
    dns.rdatatype.NS,
    dns.rdatatype.TXT,
    dns.rdatatype.SOA,
    dns.rdatatype.CNAME,
]


def lookup(domain: str) -> dict[str, list[str]]:
    """
    Perform DNS queries for a given domain and return organized results.
    
    Args:
        domain (str): The domain to query.
        
    Returns:
        dict[str, list[str]: A dictionary with record types as keys and lists of records as values.
    """
    rs = dns.resolver.Resolver()
    rs.timeout = 5
    results = defaultdict(list)
    
    for rtype in RECORDS:
        try:
            type = dns.rdatatype.to_text(rtype)
            answers = rs.resolve(domain, rtype, raise_on_no_answer=False)

            for response in answers.response.answer:
                for line in response:
                    txt = line.to_text() 

                    # Remove domain prefix from response
                    if txt.startswith(domain + '.'):
                        txt = txt[len(domain) + 1:].strip() 
                    results[type].append(txt)


        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, 
                dns.resolver.NoNameservers, dns.resolver.Timeout):
            continue

        except dns.exception.DNSException as e:
            print(f"Error querying {dns.rdatatype.to_text(rtype)}: {e}")
            continue

    return dict(results)