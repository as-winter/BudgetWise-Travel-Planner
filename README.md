# BudgetWise Travel Planner

AI-powered budget travel planner built with uAgents and ASI:One.

BudgetWise helps travelers plan affordable trips by comparing transport options, estimating travel expenses, and generating personalized itineraries based on their budget.

## Features

- Compare available transport options, including train, bus, and flight where supported.
- Estimate round-trip transport expenses.
- Calculate estimated hotel, food, and activity costs.
- Generate personalized travel itineraries using ASI:One.
- Check whether a trip fits within the user's budget.
- Handle unsupported routes and API configuration errors.

## Built With

- Python
- uAgents
- ASI:One
- OpenAI-compatible API client

## Project Files

- `agent.py` — Agent entry point.
- `protocols.py` — Travel-planning conversation workflow.
- `Travel_tools.py` — Transport data and budget calculations.
- `http_client.py` — ASI:One API helper.

## Configuration

Configure the following environment variables in your agent's runtime environment:

- `ASI1_API_KEY` — Your ASI:One API key.
- `ASI1_BASE_URL` — The API base URL specified by your ASI:One setup.

Keep API keys private. Never commit secrets to GitHub.

## Run and Test

1. Set up the Python environment and install the dependencies required by the project.
2. Configure the environment variables above.
3. Run the agent using the supported Agentverse runtime or local uAgents setup.
4. Test a supported route, such as Delhi to Jaipur, and provide the budget, number of travelers, and trip duration.
5. Review the generated itinerary and estimated budget breakdown.

## Example

A sample test for Delhi to Jaipur with two travelers and a two-day trip produced an estimated total cost of ₹6,100 against a budget of ₹8,000, leaving ₹1,900.

These are illustrative estimates from the project's sample data, not live travel prices.

## Limitations

Transport options and destination costs are based on predefined sample data. Prices and availability may differ from real-world conditions.

## Project Links

- GitHub Repository: https://github.com/as-winter/BudgetWise-Travel-Planner
- Agentverse Profile: https://agentverse.ai/agents/details/agent1qfgg5w67vyfd32t6xme6msnjhh6myd9pcmfpx8j9h9nh564x8tluxze6daa/profile

## License

No license has been specified yet.
