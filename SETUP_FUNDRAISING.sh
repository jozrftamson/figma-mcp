#!/bin/bash

# Figma MCP Server - Fundraising Setup Script
# Automatisiert das Setup für Spenden-Optionen

set -e

echo "🚀 Figma MCP Server - Fundraising Setup"
echo "======================================"
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check requirements
check_command() {
    if ! command -v $1 &> /dev/null; then
        echo "❌ $1 not found. Please install it first."
        exit 1
    fi
    echo "✅ $1 found"
}

# Step 1: Check dependencies
echo -e "${BLUE}Step 1: Checking dependencies...${NC}"
check_command git
check_command node

# Step 2: Update package.json with funding
echo ""
echo -e "${BLUE}Step 2: Updating package.json with funding options...${NC}"

# Update package.json
node -e "
const fs = require('fs');
const pkg = JSON.parse(fs.readFileSync('package.json', 'utf8'));
pkg.funding = [
  {
    'type': 'opencollective',
    'url': 'https://opencollective.com/figma-mcp'
  },
  {
    'type': 'github',
    'url': 'https://github.com/sponsors/jozrftamson'
  },
  {
    'type': 'ko-fi',
    'url': 'https://ko-fi.com/jozrftamson'
  }
];
fs.writeFileSync('package.json', JSON.stringify(pkg, null, 2) + '\n');
console.log('✅ package.json updated');
"

# Step 3: Create funding badge
echo ""
echo -e "${BLUE}Step 3: Creating funding badges...${NC}"

cat > /tmp/funding_badges.md << 'BADGES'
<!-- Add to README.md -->

## 💰 Support This Project

If you find this project useful, please consider supporting its development:

[![OpenCollective](https://img.shields.io/badge/OpenCollective-donate-blue)](https://opencollective.com/figma-mcp)
[![GitHub Sponsors](https://img.shields.io/badge/GitHub_Sponsors-sponsor-success)](https://github.com/sponsors/jozrftamson)
[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-donate-FF813F.svg?logo=buy-me-a-coffee&logoColor=white)](https://www.buymeacoffee.com/jozrftamson)
[![Ko-fi](https://img.shields.io/badge/Ko--fi-donate-FF5E8A?logo=ko-fi&logoColor=white)](https://ko-fi.com/jozrftamson)

BADGES

echo "✅ Funding badges created (see /tmp/funding_badges.md)"

# Step 4: Create URLs file
echo ""
echo -e "${BLUE}Step 4: Creating fundraising URLs file...${NC}"

cat > FUNDRAISING_URLS.txt << 'URLS'
# Figma MCP Server - Fundraising Setup Links

## Immediate Setup (Today)

1. OpenCollective Application
   URL: https://opencollective.com/apply
   Time: 5 minutes to apply, 24-48 hours approval
   Expected: Your fundraising page ready

2. GitHub Sponsors Setup
   URL: https://github.com/sponsors
   Time: 5-10 minutes
   Steps:
     a. Go to https://github.com/sponsors
     b. Click "Set up sponsor account"
     c. Configure tiers
     d. Link in profile

3. Buy Me a Coffee
   URL: https://www.buymeacoffee.com/signup
   Time: 5 minutes
   Steps:
     a. Sign up
     b. Setup profile
     c. Get share link

4. Ko-fi
   URL: https://ko-fi.com/register
   Time: 5 minutes
   Steps:
     a. Register
     b. Setup page
     c. Get widget

## Links to Update

README.md
- Add funding section with badges
- Use: /tmp/funding_badges.md content

GitHub Profile (@jozrftamson)
- Add GitHub Sponsors link
- Add Buy Me a Coffee to bio

npm Package Page
- Funding field already set in package.json
- Will show: npm fund figma-mcp

Social Media
- Twitter: Share fundraising links
- LinkedIn: Professional announcement
- GitHub Discussions: Community update

## Verification

After setup, verify:

1. GitHub Sponsors
   - Check: https://github.com/sponsors/jozrftamson

2. npm Funding
   - Run: npm fund figma-mcp

3. package.json
   - Verify "funding" field exists

4. README
   - Check sponsor section visible

## What's Next

1. Share links in communities
2. Create announcement post
3. Thank early supporters
4. Monitor funding progress

URLS

echo "✅ Fundraising URLs file created"

# Step 5: Git commit
echo ""
echo -e "${BLUE}Step 5: Committing changes...${NC}"

git add package.json
git commit -m "chore: Add funding configuration for OpenCollective, GitHub Sponsors, Ko-fi" || true

# Step 6: Final instructions
echo ""
echo -e "${GREEN}✅ Fundraising setup complete!${NC}"
echo ""
echo -e "${YELLOW}Next Steps:${NC}"
echo ""
echo "1. Setup OpenCollective (takes 24-48 hours)"
echo "   Apply here: https://opencollective.com/apply"
echo ""
echo "2. Setup GitHub Sponsors"
echo "   Go here: https://github.com/sponsors"
echo ""
echo "3. Create Buy Me a Coffee account"
echo "   Signup here: https://www.buymeacoffee.com/signup"
echo ""
echo "4. Update README with funding badges"
echo "   Copy content from: /tmp/funding_badges.md"
echo ""
echo "5. Share fundraising links"
echo "   - Twitter"
echo "   - LinkedIn"
echo "   - GitHub Discussions"
echo "   - Communities (Reddit, Dev.to, etc.)"
echo ""
echo "6. Verify npm funding"
echo "   Run: npm fund figma-mcp"
echo ""
echo -e "${BLUE}Files created:${NC}"
echo "  - FUNDRAISING.md (complete guide)"
echo "  - ECOSYSTEM_INTEGRATION.md (registry setup)"
echo "  - /tmp/funding_badges.md (README badges)"
echo "  - FUNDRAISING_URLS.txt (quick reference)"
echo ""
echo "Happy fundraising! 💚"
