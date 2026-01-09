"""
Service untuk integrasi dengan n8n self-hosted.
Mengirim data perbandingan device ke n8n untuk diproses dengan custom AI algorithm.
"""

import logging
from typing import Any, Dict, List, Optional

import requests

from .. import models
from ..core import config

# Setup logging
logger = logging.getLogger(__name__)


def send_comparison_to_n8n(
    device1: models.Phone, device2: models.Phone, rule_based_highlights: List[str]
) -> Optional[Dict[str, Any]]:
    """
    Mengirim data perbandingan device ke n8n webhook untuk AI processing.

    Args:
        device1: Device pertama
        device2: Device kedua
        rule_based_highlights: Highlights dari rule-based algorithm

    Returns:
        Dictionary berisi ai_highlights dan ai_summary dari n8n,
        atau None jika n8n disabled/error
    """
    # Check if n8n is enabled
    if not config.N8N_ENABLED:
        logger.info("n8n integration is disabled")
        return None

    # Check if webhook URL is configured
    if not config.N8N_WEBHOOK_URL:
        logger.warning("n8n webhook URL not configured")
        return None

    try:
        # Prepare payload - convert Decimal to float for JSON serialization
        payload = {
            "device_1": {
                "id": device1.id,
                "name": device1.name,
                "brand": device1.brand,
                "price": float(device1.price) if device1.price else 0,
                "cpu": device1.cpu,
                "ram": device1.ram,
                "camera": device1.camera,
                "battery": device1.battery,
                "release_year": device1.release_year,
            },
            "device_2": {
                "id": device2.id,
                "name": device2.name,
                "brand": device2.brand,
                "price": float(device2.price) if device2.price else 0,
                "cpu": device2.cpu,
                "ram": device2.ram,
                "camera": device2.camera,
                "battery": device2.battery,
                "release_year": device2.release_year,
            },
            "rule_based_highlights": rule_based_highlights,
        }

        # Send POST request to n8n webhook
        logger.info(f"Sending comparison to n8n: {device1.name} vs {device2.name}")

        response = requests.post(
            config.N8N_WEBHOOK_URL,
            json=payload,
            timeout=config.N8N_TIMEOUT,
            headers={"Content-Type": "application/json"},
        )

        # Check response status
        response.raise_for_status()

        # Parse response
        result = response.json()
        logger.info("Successfully received response from n8n")

        return result

    except requests.exceptions.Timeout:
        logger.error(f"n8n request timeout after {config.N8N_TIMEOUT} seconds")
        return None

    except requests.exceptions.ConnectionError:
        logger.error("Failed to connect to n8n webhook")
        return None

    except requests.exceptions.HTTPError as e:
        logger.error(f"n8n webhook returned HTTP error: {e}")
        return None

    except requests.exceptions.RequestException as e:
        logger.error(f"Error calling n8n webhook: {e}")
        return None

    except (KeyError, ValueError) as e:
        logger.error(f"Error parsing n8n response: {e}")
        return None


def process_n8n_response(n8n_response: Dict[str, Any]) -> Dict[str, Any]:
    """
    Memproses response dari n8n dan format ke struktur yang dibutuhkan.

    Args:
        n8n_response: Response dari n8n webhook

    Returns:
        Dictionary dengan ai_highlights dan ai_summary yang sudah diformat
    """
    try:
        # Extract highlights
        ai_highlights = n8n_response.get("ai_highlights", [])
        ai_summary = n8n_response.get("ai_summary", "")
        scores = n8n_response.get("scores", {})

        # Validate highlights structure
        if not isinstance(ai_highlights, list):
            logger.warning("Invalid ai_highlights format from n8n")
            return {"ai_highlights": [], "ai_summary": "", "scores": {}}

        # Ensure each highlight has required fields
        validated_highlights = []
        for highlight in ai_highlights:
            if isinstance(highlight, dict) and all(
                k in highlight for k in ["category", "winner", "reason"]
            ):
                validated_highlights.append(highlight)
            else:
                logger.warning(f"Invalid highlight format: {highlight}")

        return {
            "ai_highlights": validated_highlights,
            "ai_summary": ai_summary,
            "scores": scores,
        }

    except Exception as e:
        logger.error(f"Error processing n8n response: {e}")
        return {"ai_highlights": [], "ai_summary": "", "scores": {}}


def merge_highlights(
    rule_based_highlights: List[str], ai_highlights: List[Dict[str, str]]
) -> List[Dict[str, Any]]:
    """
    Menggabungkan highlights dari rule-based dan AI.

    Args:
        rule_based_highlights: List highlights sederhana (string)
        ai_highlights: List highlights dari AI (dict dengan category, winner, reason)

    Returns:
        List highlights yang sudah digabungkan dengan format unified
    """
    merged = []

    # Add AI highlights first (lebih detail)
    for highlight in ai_highlights:
        merged.append(
            {
                "category": highlight.get("category", ""),
                "winner": highlight.get("winner", ""),
                "description": highlight.get("reason", ""),
                "source": "ai",
            }
        )

    # Add rule-based highlights as fallback/additional info
    for idx, highlight in enumerate(rule_based_highlights):
        merged.append(
            {
                "category": f"📊 Perbandingan {idx + 1}",
                "winner": "",
                "description": highlight,
                "source": "rule_based",
            }
        )

    return merged


def get_ai_enhanced_highlights(
    device1: models.Phone, device2: models.Phone, rule_based_highlights: List[str]
) -> Dict[str, Any]:
    """
    Mendapatkan highlights yang sudah di-enhance dengan AI dari n8n.
    Jika n8n gagal, fallback ke rule-based highlights.

    Args:
        device1: Device pertama
        device2: Device kedua
        rule_based_highlights: Highlights dari rule-based algorithm

    Returns:
        Dictionary berisi highlights dan metadata
    """
    # Try to get AI highlights from n8n
    n8n_response = send_comparison_to_n8n(device1, device2, rule_based_highlights)

    if n8n_response:
        # Process n8n response
        processed = process_n8n_response(n8n_response)

        if processed["ai_highlights"]:
            # Success! Return AI-enhanced highlights
            return {
                "highlights": processed["ai_highlights"],
                "ai_summary": processed["ai_summary"],
                "scores": processed["scores"],
                "source": "n8n_ai",
                "fallback_used": False,
            }

    # Fallback to rule-based highlights
    logger.info("Using rule-based highlights (n8n not available)")

    # Convert rule-based highlights to structured format
    structured_highlights = []
    for idx, highlight in enumerate(rule_based_highlights):
        structured_highlights.append(
            {"category": f"📊 Highlight {idx + 1}", "winner": "", "reason": highlight}
        )

    return {
        "highlights": structured_highlights,
        "ai_summary": "Perbandingan menggunakan analisis rule-based.",
        "scores": {},
        "source": "rule_based",
        "fallback_used": True,
    }
