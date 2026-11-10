# Selenium + PyTest Test Automation Framework

[![tests](https://github.com/ashutosh0804k/selenium-pytest-framework/actions/workflows/tests.yml/badge.svg)](https://github.com/ashutosh0804k/selenium-pytest-framework/actions/workflows/tests.yml)

UI and API test automation in Python, 41 tests in total.

- **UI (29 tests):** Selenium WebDriver with the Page Object Model against [Sauce Demo](https://www.saucedemo.com). Runs on Chrome and Firefox, in parallel with `pytest-xdist`.
- **API (12 tests):** `requests` against [ReqRes](https://reqres.in). Covers users CRUD, register, login and negative cases.
- **CI:** GitHub Actions runs the UI suite on a Chrome and Firefox matrix and the API suite as its own job. Each job uploads an HTML report, and UI jobs also upload failure screenshots.

## Structure

```
config/settings.py      URLs, browser choice, timeouts (all overridable by env vars)
pages/                  Page objects: base, login, inventory, item detail, cart, checkout
utils/api_client.py     ReqRes client wrapper
tests/conftest.py       Chrome and Firefox driver fixture, screenshot on failure
tests/ui/               Login, inventory and sorting, item detail, cart, checkout
tests/api/              Users CRUD, register, login, negative cases
.github/workflows/      CI: api job plus ui job on a browser matrix
```

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

Chrome and/or Firefox must be installed. Selenium Manager downloads the matching driver automatically.

## Running

```bash
pytest                          # everything
pytest -m ui                    # browser tests only
pytest -m api                   # API tests only
pytest -m smoke                 # quick sanity set
pytest -m ui -n auto            # UI tests in parallel
BROWSER=firefox pytest -m ui    # run on Firefox (default is chrome)
HEADLESS=false pytest -m ui     # watch the browser
pytest --html=reports/report.html --self-contained-html
```

The classic ReqRes demo endpoints work without an API key, within a daily request limit. If you hit the limit, create a free key at app.reqres.in and export it. The client sends it as the `x-api-key` header:

```bash
export REQRES_API_KEY=your_key
```

## Configuration

| Variable | Default | Purpose |
|---|---|---|
| `BROWSER` | `chrome` | `chrome` or `firefox` |
| `UI_BASE_URL` | `https://www.saucedemo.com` | Site under test |
| `API_BASE_URL` | `https://reqres.in/api` | API under test |
| `REQRES_API_KEY` | empty | Optional, sent as `x-api-key` |
| `HEADLESS` | `true` | Run the browser without a window |
| `NO_SANDBOX` | `false` | Needed for Chrome in containers and CI |
| `EXPLICIT_WAIT` | `10` | Seconds for Selenium waits |

## Design notes

- Tests never touch Selenium directly. Locators and actions live in page objects, so a UI change means editing one file.
- Explicit waits only, no `time.sleep`. Page objects wait for the next page to load after a click that navigates, which removed the timing races I hit in early CI runs.
- Every test gets its own browser session, which is what makes parallel runs safe. The cost is browser start-up time per test.
- Failed UI tests save a screenshot named after the browser and test, and CI uploads them as artifacts.
- Failed API calls print the response body, so a CI failure shows the server's reason instead of only a status code.

## Known limitations

- The UI tests depend on Sauce Demo's markup and test data. If the site changes a locator or a `data-test` attribute, the matching page object needs an update.
- ReqRes has a daily request limit on keyless use, and its write endpoints (POST, PUT, DELETE) respond but do not save anything. The API tests check responses, not stored state.
- The API job runs serially on purpose, so parallel calls do not use up the ReqRes limit faster.
- Firefox runs are slower than Chrome in CI (about a minute against about half a minute for the UI suite).
- Chrome and Firefox only. Safari and Edge are not covered.
