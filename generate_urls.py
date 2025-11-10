#!/usr/bin/env python3
"""
Generate 1000 random URLs with unique domains.
URLs will have a mix of http, https, and no prefix formats.
"""

import random
import string
from typing import List, Set


def generate_random_string(length: int, use_numbers: bool = True) -> str:
    """Generate a random string of given length."""
    chars = string.ascii_lowercase
    if use_numbers:
        chars += string.digits
    return ''.join(random.choice(chars) for _ in range(length))


def generate_company_names() -> List[str]:
    """Generate realistic company/brand names."""
    # Tech-related prefixes
    tech_prefixes = [
        'tech',
        'data',
        'cloud',
        'smart',
        'digital',
        'cyber',
        'net',
        'web',
        'app',
        'soft',
        'micro',
        'meta',
        'info',
        'global',
        'secure',
        'fast',
        'quick',
        'auto',
        'super',
        'mega',
    ]

    # Business/generic prefixes
    business_prefixes = [
        'pro',
        'prime',
        'elite',
        'alpha',
        'beta',
        'nova',
        'apex',
        'zenith',
        'nexus',
        'vertex',
        'quantum',
        'crystal',
        'diamond',
        'platinum',
        'gold',
        'silver',
        'red',
        'blue',
        'green',
    ]

    # Real word prefixes
    real_words = [
        'ocean',
        'mountain',
        'river',
        'forest',
        'eagle',
        'lion',
        'tiger',
        'wolf',
        'falcon',
        'phoenix',
        'storm',
        'thunder',
        'lightning',
        'fire',
        'ice',
        'star',
        'moon',
        'sun',
        'wind',
        'earth',
        'bridge',
        'tower',
        'castle',
        'garden',
        'meadow',
        'valley',
        'peak',
        'harbor',
        'bay',
        'coast',
    ]

    # Common suffixes
    suffixes = [
        'corp',
        'labs',
        'systems',
        'solutions',
        'tech',
        'soft',
        'ware',
        'hub',
        'base',
        'link',
        'net',
        'works',
        'media',
        'group',
        'inc',
        'ltd',
        'pro',
        'plus',
        'max',
        'zone',
        'spot',
        'place',
        'space',
        'point',
        'center',
        'studio',
        'agency',
        'firm',
        'co',
        'llc',
    ]

    # Common business names
    common_names = [
        'amazon',
        'google',
        'apple',
        'microsoft',
        'facebook',
        'twitter',
        'linkedin',
        'youtube',
        'netflix',
        'spotify',
        'adobe',
        'oracle',
        'salesforce',
        'shopify',
        'stripe',
        'paypal',
        'uber',
        'airbnb',
        'tesla',
        'nvidia',
        'intel',
        'ibm',
        'cisco',
        'vmware',
        'slack',
    ]

    all_prefixes = tech_prefixes + business_prefixes + real_words
    names = []

    # Generate combination names (50%)
    for _ in range(400):
        if random.random() < 0.8:  # 80% compound names
            name = random.choice(all_prefixes) + random.choice(suffixes)
        else:  # 20% single word + suffix
            name = generate_random_string(random.randint(4, 8), False) + random.choice(
                suffixes
            )
        names.append(name)

    # Add variations of common names (20%)
    for _ in range(150):
        base_name = random.choice(common_names)
        if random.random() < 0.5:
            # Add suffix
            name = base_name + random.choice(suffixes)
        else:
            # Add prefix
            name = (
                random.choice(
                    ['my', 'get', 'use', 'try', 'go', 'new', 'old', 'big', 'small']
                )
                + base_name
            )
        names.append(name)

    # Add some single word domains (30%)
    for _ in range(200):
        if random.random() < 0.6:
            names.append(random.choice(real_words + common_names))
        else:
            names.append(generate_random_string(random.randint(5, 12), False))

    return names


def generate_tlds() -> List[str]:
    """Generate a variety of top-level domains."""
    common_tlds = ['com', 'net', 'org', 'io', 'co', 'ai', 'tech', 'app', 'dev', 'site']
    country_tlds = [
        'us',
        'uk',
        'de',
        'fr',
        'jp',
        'ca',
        'au',
        'in',
        'br',
        'ru',
        'cn',
        'kr',
        'it',
        'es',
        'nl',
        'se',
        'no',
    ]
    other_tlds = [
        'info',
        'biz',
        'online',
        'store',
        'cloud',
        'digital',
        'agency',
        'studio',
        'space',
        'world',
        'global',
        'me',
        'tv',
        'fm',
        'am',
        'xyz',
        'top',
        'pro',
        'name',
        'mobi',
        'tel',
        'travel',
        'museum',
        'aero',
    ]

    # Weight common TLDs more heavily
    tlds = common_tlds * 15 + country_tlds * 5 + other_tlds * 3
    return tlds


def generate_random_id() -> str:
    """Generate random ID numbers of various formats."""
    id_types = [
        lambda: str(random.randint(1, 999999)),  # Simple numbers
        lambda: str(random.randint(10000000, 99999999)),  # 8-digit numbers
        lambda: f"usr_{random.randint(1000, 9999)}",  # User IDs
        lambda: f"id_{random.randint(100000, 999999)}",  # Generic IDs
        lambda: f"post_{random.randint(1, 50000)}",  # Post IDs
        lambda: f"item_{random.randint(1000, 99999)}",  # Item IDs
        lambda: f"cat_{random.randint(10, 999)}",  # Category IDs
        lambda: f"{random.choice(['a', 'b', 'c', 'd', 'e'])}{random.randint(1000, 9999)}",  # Alphanumeric
        lambda: generate_random_string(8, True),  # Random string
        lambda: generate_random_string(12, True),  # Longer random string
    ]
    return random.choice(id_types)()


def generate_paths() -> List[str]:
    """Generate various URL paths."""
    # Basic paths
    basic_paths = [
        '',
        '/',
        '/home',
        '/about',
        '/contact',
        '/services',
        '/products',
        '/blog',
        '/news',
        '/support',
        '/login',
        '/register',
        '/dashboard',
        '/profile',
        '/settings',
        '/help',
        '/api/v1',
        '/api/v2',
        '/api/v3',
        '/docs',
        '/download',
        '/pricing',
        '/features',
        '/team',
        '/careers',
        '/privacy',
        '/terms',
        '/faq',
        '/search',
        '/portfolio',
        '/gallery',
        '/reviews',
    ]

    # Category paths
    category_paths = [
        '/category/tech',
        '/category/news',
        '/category/sports',
        '/category/business',
        '/category/health',
        '/category/travel',
        '/category/food',
        '/category/fashion',
        '/category/gaming',
        '/category/music',
        '/section/breaking',
        '/section/politics',
        '/section/entertainment',
        '/section/science',
        '/topic/ai',
        '/topic/blockchain',
        '/topic/startups',
        '/topic/mobile',
        '/topic/web',
    ]

    # User/admin paths
    user_paths = [
        '/user/profile',
        '/user/settings',
        '/user/dashboard',
        '/user/notifications',
        '/user/messages',
        '/admin',
        '/admin/users',
        '/admin/settings',
        '/admin/analytics',
        '/admin/reports',
        '/portal',
        '/portal/student',
        '/portal/teacher',
        '/portal/employee',
        '/account',
    ]

    # App-specific paths
    app_paths = [
        '/app',
        '/mobile',
        '/desktop',
        '/cloud',
        '/secure',
        '/beta',
        '/demo',
        '/trial',
        '/free',
        '/premium',
        '/pro',
        '/enterprise',
        '/business',
        '/personal',
        '/developer',
        '/api/auth',
        '/api/data',
        '/api/upload',
        '/api/webhook',
        '/webhook',
        '/callback',
    ]

    # E-commerce paths
    ecommerce_paths = [
        '/shop',
        '/store',
        '/cart',
        '/checkout',
        '/orders',
        '/wishlist',
        '/compare',
        '/product',
        '/deals',
        '/sale',
        '/clearance',
        '/bestsellers',
        '/new-arrivals',
    ]

    # Media/content paths
    media_paths = [
        '/watch',
        '/listen',
        '/read',
        '/view',
        '/stream',
        '/live',
        '/archive',
        '/video',
        '/audio',
        '/image',
        '/document',
        '/file',
        '/media',
        '/assets',
    ]

    all_basic = (
        basic_paths
        + category_paths
        + user_paths
        + app_paths
        + ecommerce_paths
        + media_paths
    )

    return all_basic


def generate_parameterized_paths() -> List[str]:
    """Generate paths with various parameters to make URLs longer."""
    # Search and filter parameters
    search_params = [
        '/search?q=artificial+intelligence',
        '/search?q=machine+learning',
        '/search?q=web+development',
        '/search?q=data+science',
        '/search?q=blockchain',
        '/search?q=cybersecurity',
        '/search?query=python+programming',
        '/search?query=javascript+tutorial',
        '/find?term=react+components',
        '/find?term=nodejs+framework',
    ]

    # ID-based parameters
    id_params = []
    for _ in range(30):
        path_type = random.choice(
            [
                '/page?id={}',
                '/post?id={}',
                '/article?id={}',
                '/product?id={}',
                '/user?id={}',
                '/profile?user_id={}',
                '/item?item_id={}',
                '/view?content_id={}',
            ]
        )
        id_params.append(path_type.format(generate_random_id()))

    # Multi-parameter URLs
    multi_params = []
    for _ in range(40):
        base_paths = ['/products', '/search', '/filter', '/browse', '/list', '/gallery']
        base = random.choice(base_paths)

        param_combinations = [
            f'?category={random.choice(["electronics", "clothing", "books", "sports", "home"])}&sort={random.choice(["price", "rating", "date", "popularity"])}',
            f'?page={random.randint(1, 50)}&limit={random.choice([10, 20, 50, 100])}&order={random.choice(["asc", "desc"])}',
            f'?filter={random.choice(["new", "sale", "featured", "trending"])}&price_min={random.randint(10, 100)}&price_max={random.randint(200, 1000)}',
            f'?tag={random.choice(["tech", "news", "tutorial", "review"])}&author={generate_random_id()}&date={random.randint(2020, 2024)}',
            f'?type={random.choice(["video", "image", "document", "audio"])}&size={random.choice(["small", "medium", "large"])}&format={random.choice(["jpg", "png", "pdf", "mp4"])}',
        ]

        multi_params.append(base + random.choice(param_combinations))

    # Specific content parameters
    content_params = [
        '/article?slug=getting-started-with-python',
        '/article?slug=best-practices-javascript',
        '/article?slug=machine-learning-fundamentals',
        '/article?slug=web-security-guide',
        '/blog/post?title=introduction-to-ai',
        '/blog/post?title=future-of-technology',
        '/video?v=tutorial-series-part-1',
        '/video?v=advanced-programming-techniques',
        '/course?name=full-stack-development',
        '/course?name=data-analysis-basics',
        '/event?name=tech-conference-2024',
        '/event?name=startup-meetup-berlin',
    ]

    # API endpoints with parameters
    api_params = [
        '/api/v1/users?limit=50&offset=100',
        '/api/v1/posts?category=tech&published=true',
        '/api/v2/data?format=json&include=metadata',
        '/api/v2/search?q=python&type=code',
        '/api/auth/login?redirect=/dashboard',
        '/api/upload?type=image&max_size=10mb',
        '/api/webhook?event=payment_success',
        '/api/analytics?metric=pageviews&period=30d',
    ]

    return search_params + id_params + multi_params + content_params + api_params


def generate_urls(count: int = 3000) -> List[str]:
    """Generate unique URLs."""
    company_names = generate_company_names()
    tlds = generate_tlds()
    basic_paths = generate_paths()
    param_paths = generate_parameterized_paths()

    urls = []
    used_domains: Set[str] = set()

    prefixes = ['https://', 'http://']
    prefix_weights = [0.4, 0.2, 0.4]  # 40% https, 20% http, 40% no prefix

    attempts = 0
    max_attempts = count * 10  # Prevent infinite loop

    while len(urls) < count and attempts < max_attempts:
        attempts += 1

        # Generate domain
        base_name = random.choice(company_names)
        tld = random.choice(tlds)
        domain = f"{base_name}.{tld}"

        # Skip if domain already used
        if domain in used_domains:
            continue

        used_domains.add(domain)

        # Choose prefix
        rand_val = random.random()
        if rand_val < 0.4:
            prefix = 'https://'
        elif rand_val < 0.6:
            prefix = 'http://'
        else:
            prefix = ''

        # Choose path type - 50% parameterized (longer), 50% basic
        if random.random() < 0.5:
            path = random.choice(param_paths)
        else:
            path = random.choice(basic_paths)

        # Construct URL
        url = f"{prefix}{domain}{path}"
        urls.append(url)

    return urls


def main():
    """Generate URLs and save to file."""
    print("Generating 3000 random URLs...")

    # Remove fixed seed for truly random generation
    urls = generate_urls(3000)

    # Write to file
    output_file = "/Users/igoreremin/repo/text_renderer/tlr/text/url_text.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        for url in urls:
            f.write(url + '\n')

    print(f"Generated {len(urls)} URLs and saved to {output_file}")

    # Print some statistics
    https_count = sum(1 for url in urls if url.startswith('https://'))
    http_count = sum(1 for url in urls if url.startswith('http://'))
    no_prefix_count = len(urls) - https_count - http_count
    param_count = sum(1 for url in urls if '?' in url)

    print(f"Statistics:")
    print(f"  HTTPS URLs: {https_count}")
    print(f"  HTTP URLs: {http_count}")
    print(f"  No prefix URLs: {no_prefix_count}")
    print(f"  URLs with parameters: {param_count}")

    # Show first 10 URLs as examples
    print(f"\nFirst 10 URLs:")
    for i, url in enumerate(urls[:10], 1):
        print(f"  {i:2d}. {url}")

    # Show some parameter examples
    param_urls = [url for url in urls if '?' in url][:5]
    if param_urls:
        print(f"\nSample parameterized URLs:")
        for i, url in enumerate(param_urls, 1):
            print(f"  {i}. {url}")


if __name__ == "__main__":
    main()
