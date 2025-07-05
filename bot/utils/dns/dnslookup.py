import dns.resolver
import dns.rdatatype
import dns.reversename
import dns.exception

from collections import defaultdict
from typing import Optional


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
        Dictionary with record types as keys and lists of records as values.
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


def reverse_lookup(ip: str) -> Optional[list[dict[str, list[str]]]]:
    """Perform a reverse DNS lookup for a given IP address.

    Args:
        ip (str): The IP address to reverse lookup.

    Returns:
        Dictionary with record types as keys and lists of records as values.
    """
    rs = dns.resolver.Resolver()
    rs.timeout = 5
    ptr = defaultdict(list)
    results = []
    
    try:
        reversed = dns.reversename.from_address(ip)
        answers = rs.resolve(reversed, 'PTR', raise_on_no_answer=False)
        for response in answers:
            ptr["PTR"].append(response.to_text().rstrip('.'))

        for domain in ptr["PTR"]:
            results.append(lookup(domain))

        return results

    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN,
            dns.resolver.NoNameservers, dns.resolver.Timeout):
        pass

    except dns.exception.DNSException as e:
        print(f"Error performing reverse lookup for {ip}: {e}")


if __name__ == "__main__":
    ip = "126.4.32.7"
    result = reverse_lookup(ip)
    print(result)