#!/bin/bash

# TGCR Launch Campaign - Quick Send Script
# This script extracts email templates and provides send instructions

set -e

LAUNCH_DIR="/home/elidoras-codex/luminai-genesis/docs/launch"
CAMPAIGN_LOG="/tmp/tgcr_campaign_$(date +%Y%m%d_%H%M%S).log"

echo "================================"
echo "TGCR LAUNCH CAMPAIGN - QUICK SEND"
echo "================================"
echo ""
echo "Logging to: $CAMPAIGN_LOG"
echo ""

# Check if key files exist
check_files() {
    local files=(
        "EMAIL_TEMPLATES.md"
        "STRUCTURAL_INSURRECTION_PUBLIC_ARTIFACT.md"
        "DARPA_EXECUTIVE_SUMMARY.md"
        "DARPA_TECHNICAL_PLAN.md"
        "DARPA_BUDGET_JUSTIFICATION.md"
        "TGCR_RETROFIT_ROADMAP.md"
    )

    for file in "${files[@]}"; do
        if [ ! -f "$LAUNCH_DIR/$file" ]; then
            echo "❌ Missing: $file" | tee -a "$CAMPAIGN_LOG"
            return 1
        fi
    done

    echo "✅ All launch documents present" | tee -a "$CAMPAIGN_LOG"
    return 0
}

# Extract template by number
extract_template() {
    local template_num=$1
    local file="$LAUNCH_DIR/EMAIL_TEMPLATES.md"

    # Find the template section and print it
    sed -n "/^## Template $template_num:/,/^## Template/p" "$file" | head -n -1
}

# Generate send instructions
print_send_instructions() {
    echo ""
    echo "📧 EMAIL SEND INSTRUCTIONS"
    echo "================================"
    echo ""
    echo "TIER 1: US Research Teams (Send Dec 9)"
    echo ""

    echo "1️⃣  OpenAI"
    echo "   To: partnerships@openai.com"
    echo "   CC: press@openai.com"
    echo "   Subject: The Missing Alignment Layer — TGCR Witness Protocol"
    echo "   Body: Copy Template 1 from EMAIL_TEMPLATES.md"
    echo "   Attachments: Attach STRUCTURAL_INSURRECTION_PUBLIC_ARTIFACT.md"
    echo ""

    echo "2️⃣  Anthropic"
    echo "   To: contact@anthropic.com"
    echo "   CC: press@anthropic.com"
    echo "   Subject: The Missing Alignment Layer — TGCR Witness Protocol"
    echo "   Body: Copy Template 2 from EMAIL_TEMPLATES.md"
    echo "   Attachments: Attach STRUCTURAL_INSURRECTION_PUBLIC_ARTIFACT.md"
    echo ""

    echo "3️⃣  DeepMind"
    echo "   To: research@deepmind.com"
    echo "   CC: press@deepmind.com"
    echo "   Subject: Geometric Alignment for AGI — The TGCR Framework"
    echo "   Body: Copy Template 3 from EMAIL_TEMPLATES.md"
    echo "   Attachments: Attach STRUCTURAL_INSURRECTION_PUBLIC_ARTIFACT.md"
    echo ""

    echo "TIER 2: EU/UK Funding (Send Dec 10)"
    echo ""

    echo "4️⃣  Mistral AI"
    echo "   To: contact@mistral.ai"
    echo "   Subject: European AI Safety Leadership — TGCR Integration Proposal"
    echo "   Body: Copy Template 5 from EMAIL_TEMPLATES.md"
    echo ""

    echo "5️⃣  EIC (European Innovation Council)"
    echo "   To: RTD-EIC-ENQUIRIES@ec.europa.eu"
    echo "   Subject: EIC Pathfinder Application: TGCR – Geometric AI Alignment"
    echo "   Body: Copy Template 6 from EMAIL_TEMPLATES.md"
    echo ""

    echo "6️⃣  ARIA (UK Advanced Research Agency)"
    echo "   To: contact@aria.org.uk"
    echo "   Subject: ARIA Research Program: Disruptive AI Safety — TGCR Framework"
    echo "   Body: Copy Template 7 from EMAIL_TEMPLATES.md"
    echo ""

    echo "TIER 3: Government Portals (Send Dec 11)"
    echo ""

    echo "7️⃣  DARPA"
    echo "   Portal: https://www.darpa.mil/work-with-us/opportunities"
    echo "   Submit: DARPA_EXECUTIVE_SUMMARY.md, DARPA_TECHNICAL_PLAN.md, DARPA_BUDGET_JUSTIFICATION.md"
    echo ""

    echo "8️⃣  IARPA"
    echo "   Portal: https://www.iarpa.gov/index.php/research-programs"
    echo "   Submit: Same documents as DARPA"
    echo ""

    echo "📱 Substack (Dec 9)"
    echo "   Platform: https://polkin.substack.com"
    echo "   Post: 'The Structural Insurrection' (content in SUBSTACK_CONTENT_STRATEGY.md)"
    echo ""
}

# Main execution
main() {
    echo "Step 1: Checking launch files..." | tee -a "$CAMPAIGN_LOG"
    check_files || exit 1

    echo "" | tee -a "$CAMPAIGN_LOG"
    echo "Step 2: All systems ready for launch" | tee -a "$CAMPAIGN_LOG"

    print_send_instructions | tee -a "$CAMPAIGN_LOG"

    echo ""
    echo "✅ Campaign ready to execute"
    echo ""
    echo "Next steps:"
    echo "1. Copy each email template (1-7) from EMAIL_TEMPLATES.md"
    echo "2. Send simultaneously to all recipients"
    echo "3. Track responses in EMAIL_CAMPAIGN.md tracking table"
    echo "4. Publish Substack post immediately"
    echo "5. Submit DARPA/IARPA proposals within 24 hours"
    echo ""
    echo "Campaign log: $CAMPAIGN_LOG"
}

main
