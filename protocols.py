
"""Chat protocol handlers for the BudgetWise travel planning agent."""

import re
from datetime import datetime, timezone
from uuid import uuid4

from uagents import Context, Protocol
from uagents_core.contrib.protocols.chat import (
    ChatAcknowledgement,
    ChatMessage,
    TextContent,
    chat_protocol_spec,
)
from uagents.experimental.chat_agent.protocol import build_llm_message_history

from http_client import ask_asi1
from Travel_tools import (
    calculate_trip_cost,
    get_travel_options,
    get_destination_costs,
)

travel_protocol = Protocol(spec=chat_protocol_spec)

SYSTEM_PROMPT = (
    "You are BudgetWise Travel Planner, an AI budget travel planning agent. "
    "Create practical day-by-day travel itineraries using the supplied data. "
    "Compare available transport options and respect the user's preferences. "
    "Prices are estimates, not live quotes. Never claim tickets or hotels "
    "have been booked. Never invent prices. The application adds the budget "
    "breakdown separately, so do not create another cost table. "
    "If important information is missing, ask the user for it."
)


def extract_preferences(text: str, prefs: dict) -> dict:
    lowered = text.lower()

    days = re.search(r"\b(\d+)\s*-?\s*(?:days?|nights?)\b", lowered)
    if days:
        prefs["trip_days"] = int(days.group(1))

    travelers = re.search(
        r"\b(\d+)\s*(?:adults?|people|persons?|travelers?|travellers?|of us)\b",
        lowered,
    )
    if travelers:
        prefs["travelers"] = int(travelers.group(1))

    budget = re.search(
        r"(?:under|below|within|budget(?:\s+of)?|₹|rs\.?|inr)\s*"
        r"[₹$€£]?\s*([\d,]+)",
        lowered,
    )
    if budget:
        value = budget.group(1).replace(",", "").strip()
        if value:
            prefs["budget"] = int(value)

    route = re.search(
        r"\bfrom\s+([A-Za-z ]+?)\s+to\s+"
        r"([A-Za-z ]+?)(?=\s+for\b|\s+under\b|\s+within\b|"
        r"\s+with\b|[,.!?]|$)",
        text,
        re.IGNORECASE,
    )
    if route:
        prefs["origin"] = route.group(1).strip().title()
        prefs["destination"] = route.group(2).strip().title()

    simple_route = re.search(
        r"\b(Delhi|Agra|Rishikesh|Haridwar|Jaipur)\s+to\s+"
        r"(Delhi|Agra|Rishikesh|Haridwar|Jaipur)\b",
        text,
        re.IGNORECASE,
    )
    if simple_route:
        prefs["origin"] = simple_route.group(1).title()
        prefs["destination"] = simple_route.group(2).title()

    if re.search(
        r"\b(backpack|hostel|cheapest|shoestring|super budget)\b",
        lowered,
    ):
        prefs["travel_style"] = "shoestring"
    elif re.search(r"\b(luxury|boutique|comfortable)\b", lowered):
        prefs["travel_style"] = "comfort"
    elif re.search(r"\b(mid-range|midrange|balanced)\b", lowered):
        prefs["travel_style"] = "balanced"

    return prefs


def _is_new_trip_request(text: str) -> bool:
    """Only reset saved preferences for a clear new-trip request."""
    lowered = text.lower().strip()
    return bool(
        re.search(
            r"^(?:plan|start|create|make|organize)\s+"
            r"(?:a\s+)?(?:new\s+)?(?:trip|travel|holiday|vacation)\b",
            lowered,
        )
        or re.search(r"\bstart a new trip\b", lowered)
    )


@travel_protocol.on_message(ChatMessage)
async def handle_message(ctx: Context, sender: str, msg: ChatMessage):
    await ctx.send(
        sender,
        ChatAcknowledgement(
            timestamp=datetime.now(timezone.utc),
            acknowledged_msg_id=msg.msg_id,
        ),
    )

    text = msg.text()
    if not text:
        return

    try:
        prefs = ctx.storage.get("prefs") or {}

        if _is_new_trip_request(text):
            prefs = {}

        prefs = extract_preferences(text, prefs)
        ctx.storage.set("prefs", prefs)

        origin = prefs.get("origin", "Delhi")
        destination = prefs.get("destination", "Jaipur")
        budget = prefs.get("budget", 10000)
        travelers = prefs.get("travelers", 2)
        days = prefs.get("trip_days", 2)

        trip_options = get_travel_options(origin, destination)
        destination_costs = get_destination_costs(destination)

        if not trip_options:
            response = (
                f"I don't currently have transport data for {origin} to "
                f"{destination}. Supported destinations from Delhi are "
                "Jaipur, Agra, Rishikesh, and Haridwar."
            )
        elif not destination_costs:
            response = (
                f"I don't currently have cost data for {destination}. "
                "Please try Jaipur, Agra, Rishikesh, or Haridwar."
            )
        else:
            cheapest_transport = min(
                trip_options, key=lambda option: option["cost"]
            )

            trip_cost = calculate_trip_cost(
                budget=budget,
                travellers=travelers,
                days=days,
                transport_per_person=cheapest_transport["cost"],
                hotel_per_night=destination_costs["hotel"],
                food_per_person_per_day=destination_costs["food"],
                activities_per_person=destination_costs["activities"],
            )

            preference_note = ", ".join(
                f"{key}: {value}" for key, value in sorted(prefs.items())
            ) or "none"

            messages = [
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "system",
                    "content": f"Saved traveler preferences: {preference_note}",
                },
                *build_llm_message_history(ctx),
                {"role": "user", "content": text},
                {
                    "role": "system",
                    "content": (
                        f"Origin: {origin}\n"
                        f"Destination: {destination}\n"
                        f"Budget: ₹{budget}\n"
                        f"Travelers: {travelers}\n"
                        f"Days: {days}\n"
                        f"Travel style: {prefs.get('travel_style', 'not specified')}\n"
                        f"Available transport options: {trip_options}\n"
                        f"Destination cost estimates: {destination_costs}\n"
                        f"Cheapest transport selected: {cheapest_transport}\n"
                        f"Calculated cost breakdown: {trip_cost}\n"
                        "Create a day-by-day itinerary using this data. "
                        "Do not invent prices or duplicate the budget breakdown."
                    ),
                },
            ]

            try:
                response = ask_asi1(messages)
                if not response.strip():
                    response = (
                        "The AI returned an empty response. Please try again."
                    )
                    include_breakdown = False
                else:
                    include_breakdown = True
            except Exception:
                ctx.logger.exception("ASI:One API request failed")
                response = (
                    "Sorry, the AI service is temporarily unavailable. "
                    "Please try again shortly."
                )
                include_breakdown = False

            if include_breakdown:
                response += (
                    "\n\n## Budget Breakdown (Estimated)\n"
                    f"- Transport (round trip): ₹{trip_cost['transport']:,}\n"
                    f"- Hotel: ₹{trip_cost['hotel']:,}\n"
                    f"- Food: ₹{trip_cost['food']:,}\n"
                    f"- Activities: ₹{trip_cost['activities']:,}\n"
                    f"- **Total: ₹{trip_cost['total']:,}**\n"
                    f"- **Remaining Budget: ₹{trip_cost['remaining']:,}**\n"
                    f"- Within Budget: "
                    f"{'Yes' if trip_cost['within_budget'] else 'No'}\n"
                    "- Prices are estimates, not live quotes."
                )

    except Exception:
        ctx.logger.exception("Failed to generate travel plan")
        response = (
            "Sorry, I could not generate the travel plan right now. "
            "Please check your request and try again."
        )

    await ctx.send(
        sender,
        ChatMessage(
            timestamp=datetime.now(timezone.utc),
            msg_id=uuid4(),
            content=[TextContent(type="text", text=response)],
        ),
    )


@travel_protocol.on_message(ChatAcknowledgement)
async def handle_ack(
    ctx: Context,
    sender: str,
    msg: ChatAcknowledgement,
):
    pass
