import re
from urllib.parse import urlparse, parse_qs, urlunparse

class SecurityUtils:
    SENSITIVE_KEYS = ['password', 'pass', 'pwd', 'secret', 'key', 'token', 'auth', 'uri', 'url']

    @staticmethod
    def sanitize_uri(uri: str) -> str:
        """Sanitize URIs by masking credentials and sensitive query params"""
        if not uri:
            return "***"

        try:
            parsed = urlparse(uri)

            # Mask username:password if present
            netloc = parsed.hostname or ""
            if parsed.username or parsed.password:
                if parsed.port:
                    netloc = f"***:***@{parsed.hostname}:{parsed.port}"
                else:
                    netloc = f"***:***@{parsed.hostname}"
            elif parsed.port:
                netloc = f"{parsed.hostname}:{parsed.port}"

            # Mask sensitive query params
            query_params = parse_qs(parsed.query)
            masked_query = []
            for k, v in query_params.items():
                if any(sk in k.lower() for sk in SecurityUtils.SENSITIVE_KEYS):
                    masked_query.append(f"{k}=***")
                else:
                    masked_query.append(f"{k}={v[0]}")
            
            parsed = parsed._replace(netloc=netloc, query="&".join(masked_query))
            return urlunparse(parsed)

        except Exception:
            return "***"

    @staticmethod
    def sanitize_error_message(error_msg: str, sensitive_uris=None) -> str:
        """Sanitize sensitive URIs, passwords, tokens in error messages"""
        if not error_msg:
            return error_msg

        # Replace known URIs
        if sensitive_uris:
            for uri in sensitive_uris:
                if uri:
                    error_msg = error_msg.replace(uri, SecurityUtils.sanitize_uri(uri))

        # Mask inline creds in URIs
        error_msg = re.sub(r"://([^:]+):([^@]+)@", "://***:***@", error_msg)

        # Mask sensitive key=value patterns
        patterns = [
            (r'\bpassword\s*[=:]\s*[^\s&]+', 'password=***'),
            (r'\bpass\s*[=:]\s*[^\s&]+', 'pass=***'),
            (r'\bpwd\s*[=:]\s*[^\s&]+', 'pwd=***'),
            (r'\btoken\s*[=:]\s*[^\s&]+', 'token=***'),
            (r'\bsecret\s*[=:]\s*[^\s&]+', 'secret=***'),
            (r'\bkey\s*[=:]\s*[^\s&]+', 'key=***'),
            (r'\bauth\s*[=:]\s*[^\s&]+', 'auth=***'),
        ]
        for pattern, replacement in patterns:
            error_msg = re.sub(pattern, replacement, error_msg, flags=re.IGNORECASE)

        return error_msg

    @staticmethod
    def sanitize_dict(data: dict, sensitive_keys=None) -> dict:
        """Sanitize dictionary by masking sensitive keys recursively"""
        if sensitive_keys is None:
            sensitive_keys = SecurityUtils.SENSITIVE_KEYS

        sanitized = {}
        for key, value in data.items():
            if any(sk in key.lower() for sk in sensitive_keys):
                sanitized[key] = "***"
            elif isinstance(value, dict):
                sanitized[key] = SecurityUtils.sanitize_dict(value, sensitive_keys)
            elif isinstance(value, list):
                sanitized[key] = [
                    SecurityUtils.sanitize_dict(item, sensitive_keys) if isinstance(item, dict) else "***" if isinstance(item, str) and any(sk in key.lower() for sk in sensitive_keys) else item
                    for item in value
                ]
            else:
                sanitized[key] = value
        return sanitized
