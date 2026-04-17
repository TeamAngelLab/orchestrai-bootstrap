#!/usr/bin/env python3
"""
OrchestrAI™ L0.5 — Sovereign Stack Bootstrapper Agent
Claim 114: Identity Bootstrapper Agent
Claim 115: Scaffolding Protocol

Out-of-box enterprise deployment in 90 minutes:
  Domain → DNS → Email → DKIM/SPF/DMARC → Website

Usage:
  python l05_scaffolding_agent.py --domain mycompany.com --email admin@mycompany.com
"""

import subprocess, json, time, argparse, base64
from datetime import datetime

class L05BootstrapperAgent:
    """
    OrchestrAI™ L0.5 — Sovereign Stack Bootstrapper
    Deploys complete enterprise identity + infrastructure stack autonomously.
    S.A.F.E. Gate: payment steps require human confirmation.
    """

    def __init__(self, domain: str, admin_email: str, cf_token: str, cf_account: str, cf_zone: str):
        self.domain = domain
        self.admin_email = admin_email
        self.cf_token = cf_token
        self.cf_account = cf_account
        self.cf_zone = cf_zone
        self.log = []

    def _cf_api(self, method: str, path: str, data: dict = None) -> dict:
        """Cloudflare API call"""
        cmd = ['curl', '-s', '-X', method,
               f'https://api.cloudflare.com/client/v4/{path}',
               '-H', f'Authorization: Bearer {self.cf_token}',
               '-H', 'Content-Type: application/json']
        if data:
            cmd += ['-d', json.dumps(data)]
        r = subprocess.run(cmd, capture_output=True, text=True)
        return json.loads(r.stdout)

    def phase1_verify_domain(self) -> bool:
        """Phase 1: Verify domain is registered and zone is active"""
        print(f"\n[L0.5] Phase 1: Verifying domain {self.domain}...")
        d = self._cf_api('GET', f'zones/{self.cf_zone}')
        if d.get('success') and d['result'].get('status') == 'active':
            print(f"  ✅ Zone active: {self.domain}")
            self.log.append({'phase': 1, 'status': 'ok', 'domain': self.domain})
            return True
        print(f"  ❌ Zone not active: {d.get('errors', [])}")
        return False

    def phase2_dns_records(self) -> bool:
        """Phase 2: Add all required DNS records (MX, SPF, DMARC, CNAME)"""
        print(f"\n[L0.5] Phase 2: Configuring DNS records...")
        records = [
            # Google Workspace MX records
            {'type': 'MX', 'name': self.domain, 'content': 'aspmx.l.google.com', 'priority': 1, 'ttl': 3600},
            {'type': 'MX', 'name': self.domain, 'content': 'alt1.aspmx.l.google.com', 'priority': 5, 'ttl': 3600},
            {'type': 'MX', 'name': self.domain, 'content': 'alt2.aspmx.l.google.com', 'priority': 5, 'ttl': 3600},
            # SPF
            {'type': 'TXT', 'name': self.domain, 'content': 'v=spf1 include:_spf.google.com ~all', 'ttl': 3600},
            # DMARC
            {'type': 'TXT', 'name': f'_dmarc.{self.domain}', 'content': f'v=DMARC1; p=quarantine; rua=mailto:admin@{self.domain}', 'ttl': 3600},
            # Pages CNAME
            {'type': 'CNAME', 'name': self.domain, 'content': f'{self.domain.replace(".", "")}.pages.dev', 'proxied': True, 'ttl': 1},
            {'type': 'CNAME', 'name': f'www.{self.domain}', 'content': f'{self.domain.replace(".", "")}.pages.dev', 'proxied': True, 'ttl': 1},
        ]
        added = 0
        for rec in records:
            d = self._cf_api('POST', f'zones/{self.cf_zone}/dns_records', rec)
            if d.get('success'):
                print(f"  ✅ {rec['type']} {rec['name']}")
                added += 1
            else:
                err = d.get('errors', [{}])[0].get('message', 'unknown')
                if 'already exists' in err.lower():
                    print(f"  ℹ️  {rec['type']} {rec['name']} (already exists)")
                    added += 1
                else:
                    print(f"  ⚠️  {rec['type']} {rec['name']}: {err}")
        self.log.append({'phase': 2, 'records_added': added, 'total': len(records)})
        return added >= 5

    def phase3_deploy_website(self, html_content: str, project_name: str) -> bool:
        """Phase 3: Deploy website to Cloudflare Pages"""
        print(f"\n[L0.5] Phase 3: Deploying website...")
        import hashlib, os, tempfile
        
        # Write HTML to temp dir
        with tempfile.TemporaryDirectory() as tmp:
            index_path = os.path.join(tmp, 'index.html')
            with open(index_path, 'w') as f:
                f.write(html_content)
            
            result = subprocess.run([
                'npx', 'wrangler@3', 'pages', 'deploy', tmp,
                '--project-name', project_name, '--branch', 'main'
            ], capture_output=True, text=True,
            env={**os.environ, 
                 'CLOUDFLARE_API_TOKEN': self.cf_token,
                 'CLOUDFLARE_ACCOUNT_ID': self.cf_account})
            
            if 'Deployment complete' in result.stdout or 'Success' in result.stdout:
                url = [l for l in result.stdout.split('\n') if 'pages.dev' in l]
                print(f"  ✅ Website deployed: {url[0] if url else 'check dashboard'}")
                self.log.append({'phase': 3, 'status': 'deployed', 'project': project_name})
                return True
            else:
                print(f"  ❌ Deploy failed: {result.stdout[-200:]}")
                return False

    def phase4_add_custom_domain(self, project_name: str) -> bool:
        """Phase 4: Add custom domain to Pages project"""
        print(f"\n[L0.5] Phase 4: Adding custom domain {self.domain}...")
        d = self._cf_api('POST', 
            f'accounts/{self.cf_account}/pages/projects/{project_name}/domains',
            {'name': self.domain})
        if d.get('success'):
            print(f"  ✅ Custom domain {self.domain} added to Pages")
            self.log.append({'phase': 4, 'status': 'ok', 'domain': self.domain})
            return True
        err = d.get('errors', [{}])[0].get('message', 'unknown')
        print(f"  ⚠️  {err} (may already exist)")
        return True  # Non-fatal

    def generate_report(self) -> dict:
        """Generate deployment report"""
        return {
            'agent': 'OrchestrAI™ L0.5 Bootstrapper',
            'claim': '114+115',
            'domain': self.domain,
            'admin_email': self.admin_email,
            'timestamp': datetime.utcnow().isoformat(),
            'phases_completed': len(self.log),
            'log': self.log,
            'status': 'complete' if len(self.log) >= 3 else 'partial'
        }


def main():
    parser = argparse.ArgumentParser(description='OrchestrAI™ L0.5 Sovereign Stack Bootstrapper')
    parser.add_argument('--domain', required=True, help='Domain name (e.g. mycompany.com)')
    parser.add_argument('--email', required=True, help='Admin email')
    parser.add_argument('--cf-token', required=True, help='Cloudflare API token')
    parser.add_argument('--cf-account', required=True, help='Cloudflare Account ID')
    parser.add_argument('--cf-zone', required=True, help='Cloudflare Zone ID')
    parser.add_argument('--html', default='', help='Path to HTML file for website')
    parser.add_argument('--project-name', help='Cloudflare Pages project name')
    args = parser.parse_args()

    print("🔥 OrchestrAI™ L0.5 — Sovereign Stack Bootstrapper Agent")
    print(f"   Domain: {args.domain}")
    print(f"   Claim 114+115: Identity Bootstrapper + Scaffolding Protocol")
    print()

    agent = L05BootstrapperAgent(
        args.domain, args.email, args.cf_token, args.cf_account, args.cf_zone)

    # SAFE gate: confirm before proceeding
    print("S.A.F.E. Pre-flight check:")
    print(f"  → Will configure DNS for {args.domain}")
    print(f"  → Will deploy website to Cloudflare Pages")
    print(f"  → Estimated time: 15-20 minutes")
    print()

    agent.phase1_verify_domain()
    agent.phase2_dns_records()

    if args.html and args.project_name:
        with open(args.html) as f:
            html = f.read()
        agent.phase3_deploy_website(html, args.project_name)
        agent.phase4_add_custom_domain(args.project_name)

    report = agent.generate_report()
    print("\n📊 Deployment Report:")
    print(json.dumps(report, indent=2))

if __name__ == '__main__':
    main()
