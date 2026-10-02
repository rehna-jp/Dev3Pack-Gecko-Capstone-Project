"""URL guard for SSRF protection.

Standard library only (urllib.parse, ipaddress, socket).
Refuses anything that is not https, and any host that is or resolves to a private,
loopback, link-local, reserved or multicast address.
"""

from __future__ import annotations

import ipaddress
import socket
import urllib.parse


def is_public_url(url: str) -> bool:
    """Return True if url is an https URL pointing to a publicly routable IP address.

    Decision on resolution failure: If a hostname cannot be resolved, we refuse (return False)
    as a safe default to prevent SSRF and unroutable requests.
    """
    try:
        parsed = urllib.parse.urlsplit(url)
        if parsed.scheme != "https":
            return False
        host = parsed.hostname
        if not host:
            return False

        # If host is an IP literal
        try:
            ip = ipaddress.ip_address(host)
            return ip.is_global
        except ValueError:
            pass

        # If host is a domain name, resolve all IP addresses
        # If DNS resolution fails, socket.gaierror is caught and returns False
        addr_infos = socket.getaddrinfo(host, None)
        if not addr_infos:
            return False

        for addr_info in addr_infos:
            ip_str = addr_info[4][0]
            ip = ipaddress.ip_address(ip_str)
            if not ip.is_global:
                return False

        return True
    except Exception:
        # Any parse error or resolution failure safely refuses
        return False
