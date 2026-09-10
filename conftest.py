import os
import shutil
from pathlib import Path
import logging
from pythonjsonlogger import jsonlogger
from datetime import datetime
import traceback
import json

from dotenv import load_dotenv

_log_entries = []


# Load secrets/config from a local .env file (gitignored — never committed).
# See .env.example for the expected keys.
load_dotenv()

# Non-secret Alumnium config. Defaults apply unless overridden in .env/environment.
os.environ.setdefault('ALUMNIUM_MODEL', 'openai')
os.environ.setdefault('ALUMNIUM_LOG_LEVEL', 'debug')
os.environ.setdefault('ALUMNIUM_LOG_PATH', 'alumnium.log')
os.environ.setdefault('ALUMNIUM_CACHE', 'filesystem')

# The OpenAI key must come from the environment / .env — never hardcode it.
if not os.environ.get('OPENAI_API_KEY'):
    raise RuntimeError(
        "OPENAI_API_KEY is not set. Copy .env.example to .env and add your key "
        "(or set it in your environment) before running the tests."
    )

from playwright.sync_api import sync_playwright, Page
from alumnium import Alumni
from pytest import fixture
from pytest import hookimpl
from alumnium.tools import ExecuteJavascriptTool

# Register custom markers for scenario 1 and scenario 2
def pytest_configure(config):
    config.addinivalue_line("markers", "scenario1: Run test in scenario 1")
    config.addinivalue_line("markers", "scenario2: Run test in scenario 2")

    #Setup JSON logging
    log_dir=Path("logs")
    log_dir.mkdir(exist_ok=True)

    logger=logging.getLogger("test_cases_automation")
    logger.setLevel(logging.INFO)

    #Remove existing handlers
    logger.handlers.clear()

    #Custom handler that collects logs in memory
    class ListHandler(logging.Handler):
        def emit(self, record):
            formatter=jsonlogger.JsonFormatter()
            log_entry = json.loads(formatter.format(record))
            _log_entries.append(log_entry)

    list_handler=ListHandler()
    logger.addHandler(list_handler)

    #Console handler for immdiate output
    console_handler=logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
    logger.addHandler(console_handler)

    
    # Store log file path and start time for report
    config._log_file = log_dir / f"test_run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    config._test_start_time = datetime.now()

    return logger



# Write JSON array wrapped in report at the end of test session
def pytest_sessionfinish(session, exitstatus):
    """Write all collected logs as a JSON array wrapped in a report"""
    log_file = getattr(session.config, '_log_file', None)
    start_time = getattr(session.config, '_test_start_time', datetime.now())
    
    if log_file and _log_entries:
        # Create report structure with metadata and logs array
        report = {
            "test_run": {
                "start_time": start_time.isoformat(),
                "end_time": datetime.now().isoformat(),
                "total_tests": len(_log_entries),
                "passed": len([e for e in _log_entries if e.get("status") == "passed"]),
                "failed": len([e for e in _log_entries if e.get("status") == "failed"]),
                "skipped": len([e for e in _log_entries if e.get("status") == "skipped"]),
                "exit_status": exitstatus
            },
            "logs": _log_entries  # Array of all log entries
        }
        
        try:
            with open(log_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            print(f"\n✓ Test report saved to {log_file}")
            print(f"  Total: {report['test_run']['total_tests']}, "
                  f"Passed: {report['test_run']['passed']}, "
                  f"Failed: {report['test_run']['failed']}, "
                  f"Skipped: {report['test_run']['skipped']}")
        except Exception as e:
            print(f"\n✗ Failed to save report: {e}")

@fixture(scope="session", autouse=True)
def cleanup_videos():
    """Delete all videos at the start of test session"""
    video_dir = Path("videos")
    video_dir.mkdir(exist_ok=True)  # Create directory first
    
    # Delete all files in the directory
    if video_dir.exists():
        print("Cleaning up videos directory...")
        for file in video_dir.glob("*"):
            try:
                if file.is_file():
                    file.unlink()
            except Exception as e:
                print(f"Warning: Could not delete {file}: {e}")
    yield

@fixture(scope="function")
def driver(request):
    """Playwright Chromium page; exposed as 'driver' for compatibility with tests.
    Uses Playwright's built-in video recording (no cross-thread screenshot).

    Runs headed by default (good for local debugging on Windows). Set the
    HEADLESS environment variable to 1/true to run headless (e.g. on CI)."""
    headless = os.environ.get("HEADLESS", "").strip().lower() in ("1", "true", "yes")
    video_dir = Path("videos")
    video_dir.mkdir(exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=headless,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu",
            ]
            if headless
            else None,
        )
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            ignore_https_errors=True,
            record_video_dir=str(video_dir),
            record_video_size={"width": 1920, "height": 1080},
        )
        page = context.new_page()
        try:
            yield page
        finally:
            context.close()
            try:
                video = page.video
                if video:
                    path = video.path()
                    if path and Path(path).exists():
                        dest = video_dir / f"{request.node.name.replace('::', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.webm"
                        shutil.move(str(path), str(dest))
                        print(f"[{request.node.name}] ✓ Video saved: {dest}")
            except Exception as e:
                print(f"[{request.node.name}] Video save skipped: {e}")
            browser.close()

@hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    #Get logger from logging module
    logger=logging.getLogger("test_cases_automation")

    print("Running cache")
    if report.when == "call":
        # Assuming `al` is an instance of `Alumni`.
        al = item.funcargs["al"]
        driver = item.funcargs.get("driver")

        #Extract test information for logging
        test_name=item.nodeid
        scenario=None;
        for marker in item.iter_markers():
            if marker.name.startswith("scenario"):
                scenario=marker.name.replace("scenario", "")
                break
        current_url=None;
        page_title=None;
        if driver:
            try:
                current_url = driver.url
                page_title = driver.title
            except Exception:
                pass

        #Log test result
        if report.passed:
            try:
                al.cache.save()
            except FileNotFoundError:
                pass  # alumnium cache lock file may be missing
            logger.info("Test passed", extra={
                "test_name": test_name,
                "scenario": scenario,
                "status": "passed",
                "duration": f"{report.duration:.2f}s",
                "when": report.when,
                "url": current_url,
                "page_title": page_title
            })
            print("doc saved")
        elif report.failed:
            al.cache.discard()
            
            #Extract error details
            error_type=None;
            error_message=None;
            error_traceback=None;

            if call.excinfo:
                error_type = call.excinfo.typename
                error_message = str(call.excinfo.value) if call.excinfo.value else None
                # Get formatted traceback
                error_traceback = ''.join(traceback.format_exception(
                    call.excinfo.type,
                    call.excinfo.value,
                    call.excinfo.tb
                ))

                    # Log failure with comprehensive details
            logger.error("Test failed", extra={
                "test_name": test_name,
                "scenario": scenario,
                "status": "failed",
                "duration": f"{report.duration:.2f}s",
                "when": report.when,
                "error_type": error_type,
                "error_message": error_message,
                "error_traceback": error_traceback,
                "url": current_url,
                "page_title": page_title,
                "longrepr": str(report.longrepr) if report.longrepr else None
            }, exc_info=call.excinfo)
            
        elif report.skipped:
            logger.warning("Test skipped", extra={
                "test_name": test_name,
                "scenario": scenario,
                "status": "skipped",
                "reason": str(report.longrepr) if report.longrepr else "Unknown reason",
                "when": report.when
            })




@fixture(scope="function")
def al(driver: Page):
    al = Alumni(driver, extra_tools=[ExecuteJavascriptTool])
    yield al
    al.quit()
