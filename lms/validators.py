from urllib.parse import urlparse
from rest_framework import serializers

def validate_youtube_link(value):
    """
    Валидирует ссылку, разрешая только домены youtube.com.
    """
    parsed_url = urlparse(value)
    domain = parsed_url.netloc.lower()
    if 'youtube.com' not in domain:
        raise serializers.ValidationError(f"Ссылка должна вести на YouTube ({value}).")