# Selenium + PyTest Test Automation Framework

UI and API test automation in Python.

- **UI tests** use Selenium WebDriver with the Page Object Model against [Sauce Demo](https://www.saucedemo.com).
- **API tests** use `requests` against [ReqRes](https://reqres.in).
- **CI** runs both suites on GitHub Actions and uploads HTML reports and failure screenshots.

## Structure

```
config/settings.py      URLs, credentials, timeouts (all overridable by env vars)
pages/                  Page objects: base, login, inventory, cart, checkout
utils/api_client.py     ReqRes client wrapper
tests/conftest.py       Chrome driver fixture, screenshot on failure
tests/ui/               Login, inventory/sorting, cart and checkout tests
tests/api/              Users CRUD, register and login tests
.github/workflows/      CI: separate api and ui jobs
```

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

Chrome must be installed. Selenium Manager downloads the matching driver automatically.

## Running

```bash
pytest                    # everything
pytest -m ui              # browser tests only
pytest -m api             # API tests only
pytest -m smoke           # quick sanity set
HEADLESS=false pytest -m ui   # watch the browser
pytest --html=reports/report.html --self-contained-html
```

The classic ReqRes demo endpoints work without an API key, within a daily request limit. If you hit the limit, create a free key at app.reqres.in and export it. The client sends it as the `x-api-key` header:

```bash
export REQRES_API_KEY=your_key
```

## Configuration

| Variable | Default | Purpose |
|---|---|---|
| `UI_BASE_URL` | `https://www.saucedemo.com` | Site under test |
| `API_BASE_URL` | `https://reqres.in/api` | API under test |
| `REQRES_API_KEY` | empty | Optional, sent as `x-api-key` |
| `HEADLESS` | `true` | Run Chrome without a window |
| `NO_SANDBOX` | `false` | Needed for Chrome in containers and CI |
| `EXPLICIT_WAIT` | `10` | Seconds for Selenium waits |

## Design notes

- Tests never touch Selenium directly. Locators and actions live in page objects, so a UI change means editing one file.
- Explicit waits only, no `time.sleep`.
- Failed UI tests save a screenshot to `screenshots/`, which CI uploads as an artifact.
- Tests are independent: each starts from a fresh browser session.
