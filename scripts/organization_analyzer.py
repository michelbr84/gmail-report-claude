#!/usr/bin/env python3
"""
organization_analyzer.py — Inbox Organization Advisor

Analyzes unlabeled emails, clusters them by sender/domain/subject/content
patterns, and suggests a label taxonomy with Gmail filter rules.

Usage:
    python3 organization_analyzer.py data.json --output organize.json
    python3 organization_analyzer.py data.json --output organize.json --lang pt
"""

import argparse
import json
import re
import sys
from collections import Counter, defaultdict


# ── Pattern definitions ──────────────────────────────────────────────

LABEL_PATTERNS = {
    "Newsletters": {
        "senders": ["newsletter", "news@", "digest", "weekly", "updates@", "noreply.*news"],
        "subjects": ["newsletter", "digest", "weekly", "roundup"],
        "confidence": "high",
    },
    "Receipts": {
        "senders": ["receipt", "invoice", "billing", "payment"],
        "subjects": ["receipt", "invoice", "order confirmation", "payment received", "your order"],
        "confidence": "high",
    },
    "Finance": {
        "domains": ["bank", "chase", "wellsfargo", "paypal", "stripe", "wise", "revolut", "nubank", "itau", "bradesco", "santander"],
        "subjects": ["statement", "transaction", "transfer", "balance", "deposit"],
        "confidence": "high",
    },
    "Travel": {
        "domains": ["booking.com", "airbnb", "expedia", "kayak", "airlines", "latam", "gol", "azul"],
        "subjects": ["booking", "reservation", "flight", "itinerary", "check-in", "boarding"],
        "confidence": "medium",
    },
    "Shopping": {
        "domains": ["amazon", "mercadolivre", "shopee", "aliexpress", "ebay", "etsy", "shopify"],
        "subjects": ["order", "shipped", "delivered", "tracking", "dispatch"],
        "confidence": "high",
    },
    "Security": {
        "subjects": ["verification", "2fa", "two-factor", "security alert", "login attempt", "password reset", "suspicious"],
        "senders": ["security", "noreply.*auth", "no-reply.*verify"],
        "confidence": "high",
    },
    "Notifications": {
        "senders": ["notifications@", "notify@", "alerts@", "noreply@", "no-reply@", "mailer-daemon"],
        "subjects": ["notification", "alert", "reminder"],
        "confidence": "high",
    },
    "Subscriptions": {
        "subjects": ["subscription", "renewal", "trial", "plan", "membership", "upgrade"],
        "senders": ["billing", "subscription"],
        "confidence": "medium",
    },
    "AI Tools": {
        "domains": ["openai", "anthropic", "claude", "chatgpt", "midjourney", "github.com", "vercel", "netlify", "huggingface"],
        "senders": ["copilot", "codespaces"],
        "confidence": "medium",
    },
    "Social": {
        "domains": ["linkedin", "twitter", "facebook", "instagram", "tiktok", "reddit", "discord"],
        "subjects": ["mentioned you", "liked your", "commented on", "new follower", "connection"],
        "confidence": "high",
    },
}

# Portuguese translations
PT_LABELS = {
    "Newsletters": "Newsletters",
    "Receipts": "Recibos",
    "Finance": "Finanças",
    "Travel": "Viagens",
    "Shopping": "Compras",
    "Security": "Segurança",
    "Notifications": "Notificações",
    "Subscriptions": "Assinaturas",
    "AI Tools": "Ferramentas IA",
    "Social": "Redes Sociais",
    "Work": "Trabalho",
    "Family": "Família",
    "Follow Up": "Acompanhar",
}

PT_CONFIDENCE = {"high": "alta", "medium": "média", "low": "baixa"}

PT_STRINGS = {
    "overview_title": "Visão Geral",
    "taxonomy_title": "Taxonomia de Labels Sugerida",
    "examples_title": "Exemplos por Cluster",
    "filters_title": "Filtros Gmail Sugeridos",
    "score_title": "Score de Organização",
    "label": "Label",
    "rationale": "Motivo",
    "volume": "Volume Estimado",
    "confidence": "Confiança",
    "sender": "Remetente",
    "subject": "Assunto",
    "date": "Data",
    "criteria": "Critério",
    "action": "Ação",
    "apply_label": "Aplicar label",
    "total_analyzed": "Total de emails analisados",
    "unlabeled": "Sem label útil",
    "clusters_found": "Clusters encontrados",
    "current_score": "Organização atual",
    "opportunity": "Oportunidade de melhoria",
}

EN_STRINGS = {
    "overview_title": "Overview",
    "taxonomy_title": "Suggested Label Taxonomy",
    "examples_title": "Cluster Examples",
    "filters_title": "Suggested Gmail Filters",
    "score_title": "Organization Score",
    "label": "Label",
    "rationale": "Rationale",
    "volume": "Estimated Volume",
    "confidence": "Confidence",
    "sender": "Sender",
    "subject": "Subject",
    "date": "Date",
    "criteria": "Criteria",
    "action": "Action",
    "apply_label": "Apply label",
    "total_analyzed": "Total emails analyzed",
    "unlabeled": "Without useful label",
    "clusters_found": "Clusters found",
    "current_score": "Current organization",
    "opportunity": "Improvement opportunity",
}


def extract_email(from_header):
    """Extract email address from a From header."""
    match = re.search(r"<([^>]+)>", from_header)
    if match:
        return match.group(1).lower()
    match = re.search(r"[\w.+-]+@[\w-]+\.[\w.-]+", from_header)
    if match:
        return match.group(0).lower()
    return from_header.lower().strip()


def extract_domain(email):
    """Extract domain from email address."""
    parts = email.split("@")
    return parts[1] if len(parts) == 2 else email


def is_unlabeled(msg):
    """Check if message lacks useful custom labels."""
    labels = msg.get("labels", [])
    system_labels = {
        "INBOX", "UNREAD", "IMPORTANT", "STARRED", "SENT", "DRAFT",
        "TRASH", "SPAM", "CATEGORY_PERSONAL", "CATEGORY_SOCIAL",
        "CATEGORY_PROMOTIONS", "CATEGORY_UPDATES", "CATEGORY_FORUMS",
    }
    custom_labels = [l for l in labels if l not in system_labels]
    return len(custom_labels) == 0


def match_patterns(msg, patterns):
    """Check if a message matches a pattern definition."""
    email = extract_email(msg.get("from", ""))
    domain = extract_domain(email)
    subject = msg.get("subject", "").lower()
    from_lower = msg.get("from", "").lower()

    # Check sender patterns
    for pattern in patterns.get("senders", []):
        if re.search(pattern, from_lower):
            return True

    # Check domain patterns
    for pattern in patterns.get("domains", []):
        if pattern in domain:
            return True

    # Check subject patterns
    for pattern in patterns.get("subjects", []):
        if pattern in subject:
            return True

    return False


def cluster_messages(messages):
    """Cluster unlabeled messages into suggested label groups."""
    clusters = defaultdict(list)
    unclustered = []

    for msg in messages:
        matched = False
        for label_name, patterns in LABEL_PATTERNS.items():
            if match_patterns(msg, patterns):
                clusters[label_name].append(msg)
                matched = True
                break

        if not matched:
            unclustered.append(msg)

    # Try to cluster remaining by domain
    domain_groups = defaultdict(list)
    for msg in unclustered:
        email = extract_email(msg.get("from", ""))
        domain = extract_domain(email)
        domain_groups[domain].append(msg)

    # Domains with 3+ messages become their own clusters
    for domain, msgs in domain_groups.items():
        if len(msgs) >= 3:
            label_name = domain.split(".")[0].title()
            clusters[label_name].extend(msgs)
        else:
            # Truly unclustered
            clusters["_unclustered"].extend(msgs)

    return dict(clusters)


def generate_filter_suggestions(clusters, lang="en"):
    """Generate Gmail filter rule suggestions for each cluster."""
    filters = []

    for label_name, messages in clusters.items():
        if label_name == "_unclustered":
            continue

        # Find common senders / domains
        sender_counts = Counter()
        domain_counts = Counter()
        for msg in messages:
            email = extract_email(msg.get("from", ""))
            sender_counts[email] += 1
            domain_counts[extract_domain(email)] += 1

        top_domains = [d for d, c in domain_counts.most_common(5) if c >= 2]
        top_senders = [s for s, c in sender_counts.most_common(5) if c >= 2]

        if top_domains:
            criteria = " OR ".join(f"from:@{d}" for d in top_domains)
        elif top_senders:
            criteria = " OR ".join(f"from:{s}" for s in top_senders[:3])
        else:
            continue

        display_label = PT_LABELS.get(label_name, label_name) if lang == "pt" else label_name

        filters.append({
            "label": display_label,
            "criteria": criteria,
            "action": f"Apply label: {display_label}",
            "message_count": len(messages),
        })

    return filters


def calculate_organization_score(total, unlabeled, clusters):
    """Calculate inbox organization score (0-100)."""
    if total == 0:
        return 100

    labeled_ratio = 1 - (unlabeled / total)
    cluster_coverage = sum(
        len(msgs) for name, msgs in clusters.items() if name != "_unclustered"
    )
    coverage_ratio = cluster_coverage / unlabeled if unlabeled > 0 else 1

    # Score: 60% based on current labeling, 40% on cluster quality
    score = int((labeled_ratio * 60) + (coverage_ratio * 40))
    return min(100, max(0, score))


def main():
    parser = argparse.ArgumentParser(description="Analyze inbox organization")
    parser.add_argument("input", help="Input Gmail data JSON file")
    parser.add_argument("--output", default="organize.json", help="Output file")
    parser.add_argument("--lang", default="en", choices=["en", "pt"], help="Report language")
    parser.add_argument("--examples", type=int, default=5, help="Examples per cluster")

    args = parser.parse_args()
    strings = PT_STRINGS if args.lang == "pt" else EN_STRINGS

    with open(args.input, "r", encoding="utf-8") as f:
        data = json.load(f)

    messages = data.get("messages", [])
    total = len(messages)

    # Filter to unlabeled
    unlabeled_msgs = [m for m in messages if is_unlabeled(m)]
    unlabeled_count = len(unlabeled_msgs)

    print(f"Total: {total} | Unlabeled: {unlabeled_count} ({round(unlabeled_count/total*100, 1) if total else 0}%)")

    # Cluster
    clusters = cluster_messages(unlabeled_msgs)
    active_clusters = {k: v for k, v in clusters.items() if k != "_unclustered"}

    # Build taxonomy
    taxonomy = []
    for label_name, msgs in sorted(active_clusters.items(), key=lambda x: len(x[1]), reverse=True):
        confidence = LABEL_PATTERNS.get(label_name, {}).get("confidence", "low")
        display_label = PT_LABELS.get(label_name, label_name) if args.lang == "pt" else label_name
        display_confidence = PT_CONFIDENCE.get(confidence, confidence) if args.lang == "pt" else confidence

        examples = []
        for msg in msgs[:args.examples]:
            examples.append({
                "from": msg.get("from", ""),
                "subject": msg.get("subject", ""),
                "date": msg.get("date", "")[:16],
            })

        taxonomy.append({
            "label": display_label,
            "rationale": f"Matched {len(msgs)} messages by sender/subject patterns",
            "volume": len(msgs),
            "confidence": display_confidence,
            "examples": examples,
        })

    # Filters
    filter_suggestions = generate_filter_suggestions(clusters, args.lang)

    # Score
    org_score = calculate_organization_score(total, unlabeled_count, clusters)
    unclustered_count = len(clusters.get("_unclustered", []))

    result = {
        "language": args.lang,
        "overview": {
            "total_analyzed": total,
            "unlabeled_count": unlabeled_count,
            "unlabeled_percentage": round(unlabeled_count / total * 100, 1) if total else 0,
            "clusters_found": len(active_clusters),
            "unclustered": unclustered_count,
        },
        "taxonomy": taxonomy,
        "filter_suggestions": filter_suggestions,
        "organization_score": {
            "current": org_score,
            "opportunity": 100 - org_score,
        },
    }

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"Clusters: {len(active_clusters)} | Unclustered: {unclustered_count}")
    print(f"Organization Score: {org_score}/100")
    print(f"Results saved to {args.output}")


if __name__ == "__main__":
    main()
