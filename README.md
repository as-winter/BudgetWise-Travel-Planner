# BudgetWise Travel Planner

An AI-powered travel planning agent that helps budget-conscious travelers plan affordable trips with personalized itineraries and estimated travel expenses.

## Overview

BudgetWise Travel Planner is built using Python, uAgents, and ASI:One. Users can provide their origin, destination, trip duration, number of travelers, and total budget.

The agent compares available transport options, generates a day-wise itinerary, and provides an estimated cost breakdown to help users understand whether their trip fits within their budget.

## Features

- **Transport Option Comparison:** Compares available transport options with estimated costs and travel durations for supported routes.
- **Trip Cost Estimation:** Calculates estimated transportation, accommodation, food, and activity expenses.
- **Personalized Itineraries:** Generates day-wise travel plans based on the user's destination and trip requirements.
- **Budget Breakdown:** Shows the estimated total cost and remaining budget.
- **Conversational Travel Planning:** Allows users to interact with the agent through ASI:One chat.

## Technologies Used

- Python
- uAgents
- ASI:One
- Agentverse

## Example

**User Request:**

Plan a 2-day trip from Delhi to Jaipur for 2 travelers with a total budget of ₹8,000. Compare transport options, create a day-wise itinerary, and provide a detailed budget breakdown.

**Sample Estimated Budget:**

| Expense | Estimated Cost |
|---|---:|
| Transport | ₹1,800 |
| Hotel | ₹700 |
| Food | ₹2,000 |
| Activities | ₹1,600 |
| **Total** | **₹6,100** |
| **Remaining Budget** | **₹1,900** |

*These figures are illustrative estimates based on the project's sample data.*

## Project Structure

- `agent.py` — Agent entry point and protocol registration.
- `protocols.py` — Handles travel planning conversations and requests.
- `Travel_tools.py` — Contains transport data and budget calculation tools.
- `http_client.py` — ASI:One API helper.

## Setup and Usage

The agent is configured and run through Agentverse.

1. Configure the required ASI:One credentials in the Agentverse environment.
2. Register and activate the agent.
3. Open the agent through ASI:One.
4. Enter a travel request with the origin, destination, duration, number of travelers, and budget.
5. Review the generated itinerary and estimated budget breakdown.

## Limitations

- Travel costs are estimates based on predefined sample data and AI-generated recommendations, not live prices.
- Transport options are available only for supported routes.
- The agent does not book trips or fetch real-time flight or hotel availability.
- Users should confirm actual fares and rates before making travel arrangements.

## Links

- **GitHub Repository:** https://github.com/as-winter/BudgetWise-Travel-Planner
- **Agentverse Profile:** https://agentverse.ai/agents/details/agent1qfgg5w67vyfd32t6xme6msnjhh6myd9pcmfpx8j9h9nh564x8tluxze6daa/profile

## Project Goal

BudgetWise aims to make travel planning simpler, smarter, and more affordable by combining AI-generated recommendations with transparent budget calculations.
