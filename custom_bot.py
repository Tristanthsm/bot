import os
import json
import argparse
import requests


def extract_webhook_info(workflow_file: str):
    with open(workflow_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    for node in data.get('nodes', []):
        if node.get('type') == 'n8n-nodes-base.webhook':
            path = node.get('parameters', {}).get('path', '')
            webhook_id = node.get('webhookId')
            if path is not None and webhook_id is not None:
                return path, webhook_id
    raise ValueError('No webhook node found in workflow')


def build_webhook_url(base_url: str, webhook_id: str, path: str) -> str:
    base_url = base_url.rstrip('/')
    if not path.startswith('/'):
        path = '/' + path
    return f"{base_url}/webhook/{webhook_id}{path}"


def main():
    parser = argparse.ArgumentParser(description='Send POST request to n8n webhook')
    parser.add_argument('--workflow', default='workflow.json', help='Path to workflow JSON file')
    parser.add_argument('--url', help='Full webhook URL. Overrides workflow parsing')
    parser.add_argument('--base-url', default=os.getenv('WEBHOOK_BASE_URL', 'http://localhost:5678'),
                        help='Base URL for webhook (when not using --url)')
    parser.add_argument('--data-url', default='https://example.com',
                        help='URL parameter to send to the webhook')
    args = parser.parse_args()

    if args.url:
        webhook_url = args.url
    else:
        path, webhook_id = extract_webhook_info(args.workflow)
        webhook_url = build_webhook_url(args.base_url, webhook_id, path)

    response = requests.post(webhook_url, params={'url': args.data_url})
    print(response.text)


if __name__ == '__main__':
    main()
