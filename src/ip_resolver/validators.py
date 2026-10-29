from dataclasses import dataclass

import dns.exception
import dns.resolver

@dataclass(frozen =True)
class TopLevelDomainResult:
    tld: str
    syntax_valid: bool
    exists: bool

def validate_top_level_domain(hostname: str) -> TopLevelDomainResult:
    """
    Validate the top-level domain (TLD) of a given hostname.

    Args:
        hostname (str): The hostname to validate.

    Returns:
        TopLevelDomainResult: A dataclass containing the TLD, syntax validity, and existence status.
    """
    parts = hostname.strip().lower().split('.')

    if len(parts)< 2:
        return TopLevelDomainResult(
            tld= "",
            syntax_valid= False,
            exists= False,
        )


    tld = parts[-1]
    syntax_valid= tld.isalpha() and 2<= len(tld) <= 63

    if not syntax_valid:
        return TopLevelDomainResult(
            tld = tld,
            syntax_valid = False,
            exists = False,
        )

    try:
        dns.resolver.resolve(tld, "NS")
    except dns.exception.DNSException:
        return TopLevelDomainResult(
            tld = tld,
            syntax_valid = True,
            exists = False,
        )

    return TopLevelDomainResult(
        tld = tld,
        syntax_valid = True,
        exists = True,
    )